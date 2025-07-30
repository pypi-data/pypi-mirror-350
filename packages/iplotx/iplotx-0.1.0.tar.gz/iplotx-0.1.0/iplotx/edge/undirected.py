from math import atan2, tan, cos, pi, sin
from collections import defaultdict
import numpy as np
import matplotlib as mpl

from .common import _compute_loops_per_angle
from .label import LabelCollection
from ..utils.matplotlib import (
    _compute_mid_coord,
    _stale_wrapper,
)


class UndirectedEdgeCollection(mpl.collections.PatchCollection):
    def __init__(self, *args, **kwargs):
        kwargs["match_original"] = True
        self._vertex_ids = kwargs.pop("vertex_ids", None)
        self._vertex_centers = kwargs.pop("vertex_centers", None)
        self._vertex_paths = kwargs.pop("vertex_paths", None)
        self._style = kwargs.pop("style", None)
        self._labels = kwargs.pop("labels", None)
        super().__init__(*args, **kwargs)

    @staticmethod
    def _get_edge_vertex_sizes(edge_vertices):
        sizes = []
        for visual_vertex in edge_vertices:
            if visual_vertex.size is not None:
                sizes.append(visual_vertex.size)
            else:
                sizes.append(max(visual_vertex.width, visual_vertex.height))
        return sizes

    @staticmethod
    def _compute_edge_angles(path, trans):
        """Compute edge angles for both starting and ending vertices.

        NOTE: The domain of atan2 is (-pi, pi].
        """
        positions = trans(path.vertices)

        # first angle
        x1, y1 = positions[0]
        x2, y2 = positions[1]
        angle1 = atan2(y2 - y1, x2 - x1)

        # second angle
        x1, y1 = positions[-1]
        x2, y2 = positions[-2]
        angle2 = atan2(y2 - y1, x2 - x1)
        return (angle1, angle2)

    def _compute_paths(self, transform=None):
        """Compute paths for the edges.

        Loops split the largest wedge left open by other
        edges of that vertex. The algo is:
        (i) Find what vertices each loop belongs to
        (ii) While going through the edges, record the angles
             for vertices with loops
        (iii) Plot each loop based on the recorded angles
        """
        vids = self._vertex_ids
        vpaths = self._vertex_paths
        vcenters = self._vertex_centers
        if transform is None:
            transform = self.get_transform()
        trans = transform.transform
        trans_inv = transform.inverted().transform

        # 1. Make a list of vertices with loops, and store them for later
        loop_vertex_dict = {}
        for i, (v1, v2) in enumerate(vids):
            if v1 != v2:
                continue
            if v1 not in loop_vertex_dict:
                loop_vertex_dict[v1] = {
                    "indices": [],
                    "edge_angles": [],
                }
            loop_vertex_dict[v1]["indices"].append(i)

        # 2. Make paths for non-loop edges
        # NOTE: keep track of parallel edges to offset them
        parallel_edges = defaultdict(list)

        # Get actual coordinates of the vertex border
        paths = []
        for i, (v1, v2) in enumerate(vids):
            # Postpone loops (step 3)
            if v1 == v2:
                paths.append(None)
                continue

            # Coordinates of the adjacent vertices, in data coords
            vcoord_data = vcenters[i]

            # Coordinates in figure (default) coords
            vcoord_fig = trans(vcoord_data)

            # Vertex paths in figure (default) coords
            vpath_fig = vpaths[i]

            # Shorten edge
            if not self._style.get("curved", False):
                path = self._shorten_path_undirected_straight(
                    vcoord_fig,
                    vpath_fig,
                    trans_inv,
                )
            else:
                path = self._shorten_path_undirected_curved(
                    vcoord_fig,
                    vpath_fig,
                    trans_inv,
                    tension=self._style.get("tension", 1.5),
                )

            # Collect angles for this vertex, to be used for loops plotting below
            if (v1 in loop_vertex_dict) or (v2 in loop_vertex_dict):
                angles = self._compute_edge_angles(
                    path,
                    trans,
                )
                if v1 in loop_vertex_dict:
                    loop_vertex_dict[v1]["edge_angles"].append(angles[0])
                if v2 in loop_vertex_dict:
                    loop_vertex_dict[v2]["edge_angles"].append(angles[1])

            # Add the path for this non-loop edge
            paths.append(path)
            # FIXME: curved parallel edges depend on the direction of curvature...!
            parallel_edges[(v1, v2)].append(i)

        # Fix parallel edges
        # If none found, empty the dictionary already
        if max(parallel_edges.values(), key=len) == 1:
            parallel_edges = {}
        if not self._style.get("curved", False):
            while len(parallel_edges) > 0:
                (v1, v2), indices = parallel_edges.popitem()
                indices_inv = parallel_edges.pop((v2, v1), [])
                nparallel = len(indices)
                nparallel_inv = len(indices_inv)
                ntot = len(indices) + len(indices_inv)
                if ntot > 1:
                    self._fix_parallel_edges_straight(
                        paths,
                        indices,
                        indices_inv,
                        trans,
                        trans_inv,
                        offset=self._style.get("offset", 3),
                    )

        # 3. Deal with loops at the end
        for vid, ldict in loop_vertex_dict.items():
            vpath = vpaths[ldict["indices"][0]][0]
            vcoord_fig = trans(vcenters[ldict["indices"][0]][0])
            nloops = len(ldict["indices"])
            edge_angles = ldict["edge_angles"]

            # The space between the existing angles is where we can fit the loops
            # One loop we can fit in the largest wedge, multiple loops we need
            nloops_per_angle = _compute_loops_per_angle(nloops, edge_angles)

            idx = 0
            for theta1, theta2, nloops in nloops_per_angle:
                # Angular size of each loop in this wedge
                delta = (theta2 - theta1) / nloops

                # Iterate over individual loops
                for j in range(nloops):
                    thetaj1 = theta1 + j * delta
                    # Use 60 degrees as the largest possible loop wedge
                    thetaj2 = thetaj1 + min(delta, pi / 3)

                    # Get the path for this loop
                    path = self._compute_loop_path(
                        vcoord_fig,
                        vpath,
                        thetaj1,
                        thetaj2,
                        trans_inv,
                    )
                    paths[ldict["indices"][idx]] = path
                    idx += 1

        return paths

    def _fix_parallel_edges_straight(
        self,
        paths,
        indices,
        indices_inv,
        trans,
        trans_inv,
        offset=3,
    ):
        """Offset parallel edges along the same path."""
        ntot = len(indices) + len(indices_inv)

        # This is straight so two vertices anyway
        # NOTE: all paths will be the same, which is why we need to offset them
        vs, ve = trans(paths[indices[0]].vertices)

        # Move orthogonal to the line
        fracs = (
            (vs - ve) / np.sqrt(((vs - ve) ** 2).sum()) @ np.array([[0, 1], [-1, 0]])
        )

        # NOTE: for now treat both direction the same
        for i, idx in enumerate(indices + indices_inv):
            # Offset the path
            paths[idx].vertices = trans_inv(
                trans(paths[idx].vertices) + fracs * offset * (i - ntot / 2)
            )

    def _compute_loop_path(
        self,
        vcoord_fig,
        vpath,
        angle1,
        angle2,
        trans_inv,
    ):
        # Shorten at starting angle
        start = _get_shorter_edge_coords(vpath, angle1) + vcoord_fig
        # Shorten at end angle
        end = _get_shorter_edge_coords(vpath, angle2) + vcoord_fig

        aux1 = (start - vcoord_fig) * 2.5 + vcoord_fig
        aux2 = (end - vcoord_fig) * 2.5 + vcoord_fig

        vertices = np.vstack(
            [
                start,
                aux1,
                aux2,
                end,
            ]
        )
        codes = ["MOVETO"] + ["CURVE4"] * 3

        # Offset to place and transform to data coordinates
        vertices = trans_inv(vertices)
        codes = [getattr(mpl.path.Path, x) for x in codes]
        path = mpl.path.Path(
            vertices,
            codes=codes,
        )
        return path

    def _shorten_path_undirected_straight(
        self,
        vcoord_fig,
        vpath_fig,
        trans_inv,
    ):
        # Straight SVG instructions
        path = {
            "vertices": [],
            "codes": ["MOVETO", "LINETO"],
        }

        # Angle of the straight line
        theta = atan2(*((vcoord_fig[1] - vcoord_fig[0])[::-1]))

        # Shorten at starting vertex
        vs = _get_shorter_edge_coords(vpath_fig[0], theta) + vcoord_fig[0]
        path["vertices"].append(vs)

        # Shorten at end vertex
        ve = _get_shorter_edge_coords(vpath_fig[1], theta + pi) + vcoord_fig[1]
        path["vertices"].append(ve)

        path = mpl.path.Path(
            path["vertices"],
            codes=[getattr(mpl.path.Path, x) for x in path["codes"]],
        )
        path.vertices = trans_inv(path.vertices)
        return path

    def _shorten_path_undirected_curved(
        self,
        vcoord_fig,
        vpath_fig,
        trans_inv,
        tension=+1.5,
    ):
        # Angle of the straight line
        theta = atan2(*((vcoord_fig[1] - vcoord_fig[0])[::-1]))

        # Shorten at starting vertex
        vs = _get_shorter_edge_coords(vpath_fig[0], theta) + vcoord_fig[0]

        # Shorten at end vertex
        ve = _get_shorter_edge_coords(vpath_fig[1], theta + pi) + vcoord_fig[1]

        edge_straight_length = np.sqrt(((ve - vs) ** 2).sum())

        aux1 = vs + 0.33 * (ve - vs)
        aux2 = vs + 0.67 * (ve - vs)

        # Move Bezier points orthogonal to the line
        fracs = (
            (vs - ve) / np.sqrt(((vs - ve) ** 2).sum()) @ np.array([[0, 1], [-1, 0]])
        )
        aux1 += 0.1 * fracs * tension * edge_straight_length
        aux2 += 0.1 * fracs * tension * edge_straight_length

        path = {
            "vertices": [
                vs,
                aux1,
                aux2,
                ve,
            ],
            "codes": ["MOVETO"] + ["CURVE4"] * 3,
        }

        path = mpl.path.Path(
            path["vertices"],
            codes=[getattr(mpl.path.Path, x) for x in path["codes"]],
        )
        path.vertices = trans_inv(path.vertices)
        return path

    def _compute_labels(self):
        style = self._style.get("label", None) if self._style is not None else None
        offsets = []
        for path in self._paths:
            offset = _compute_mid_coord(path)
            offsets.append(offset)

        if not hasattr(self, "_label_collection"):
            self._label_collection = LabelCollection(
                self._labels,
                style=style,
            )

            # Forward a bunch of mpl settings that are needed
            self._label_collection.set_figure(self.figure)
            self._label_collection.axes = self.axes
            # forward the clippath/box to the children need this logic
            # because mpl exposes some fast-path logic
            clip_path = self.get_clip_path()
            if clip_path is None:
                clip_box = self.get_clip_box()
                self._label_collection.set_clip_box(clip_box)
            else:
                self._label_collection.set_clip_path(clip_path)

            # Finally make the patches
            self._label_collection._create_labels()
        self._label_collection.set_offsets(offsets)

    def get_children(self):
        children = []
        if hasattr(self, "_label_collection"):
            children.append(self._label_collection)
        return children

    @_stale_wrapper
    def draw(self, renderer, *args, **kwds):
        if self._vertex_paths is not None:
            self._paths = self._compute_paths()
            if self._labels is not None:
                self._compute_labels()
        super().draw(renderer)

        for child in self.get_children():
            child.draw(renderer, *args, **kwds)

    @property
    def stale(self):
        return super().stale

    @stale.setter
    def stale(self, val):
        mpl.collections.PatchCollection.stale.fset(self, val)
        if val and hasattr(self, "stale_callback_post"):
            self.stale_callback_post(self)


def make_stub_patch(**kwargs):
    """Make a stub undirected edge patch, without actual path information."""
    kwargs["clip_on"] = kwargs.get("clip_on", True)
    if ("color" in kwargs) and ("edgecolor" not in kwargs):
        kwargs["edgecolor"] = kwargs.pop("color")
    # Edges are always hollow, because they are not closed paths
    kwargs["facecolor"] = "none"

    # Forget specific properties that are not supported here
    forbidden_props = [
        "curved",
        "tension",
        "offset",
        "label",
    ]
    for prop in forbidden_props:
        if prop in kwargs:
            kwargs.pop(prop)

    # NOTE: the path is overwritten later anyway, so no reason to spend any time here
    art = mpl.patches.PathPatch(
        mpl.path.Path([[0, 0]]),
        **kwargs,
    )
    return art


def _get_shorter_edge_coords(vpath, theta):
    # Bound theta from -pi to pi (why is that not guaranteed?)
    theta = (theta + pi) % (2 * pi) - pi

    for i in range(len(vpath)):
        v1 = vpath.vertices[i]
        v2 = vpath.vertices[(i + 1) % len(vpath)]
        theta1 = atan2(*((v1)[::-1]))
        theta2 = atan2(*((v2)[::-1]))

        # atan2 ranges ]-3.14, 3.14]
        # so it can be that theta1 is -3 and theta2 is +3
        # therefore we need two separate cases, one that cuts at pi and one at 0
        cond1 = theta1 <= theta <= theta2
        cond2 = (
            (theta1 + 2 * pi) % (2 * pi)
            <= (theta + 2 * pi) % (2 * pi)
            <= (theta2 + 2 * pi) % (2 * pi)
        )
        if cond1 or cond2:
            break
    else:
        raise ValueError("Angle for patch not found")

    # The edge meets the patch of the vertex on the v1-v2 size,
    # at angle theta from the center
    mtheta = tan(theta)
    if v2[0] == v1[0]:
        xe = v1[0]
    else:
        m12 = (v2[1] - v1[1]) / (v2[0] - v1[0])
        xe = (v1[1] - m12 * v1[0]) / (mtheta - m12)
    ye = mtheta * xe
    ve = np.array([xe, ye])
    return ve
