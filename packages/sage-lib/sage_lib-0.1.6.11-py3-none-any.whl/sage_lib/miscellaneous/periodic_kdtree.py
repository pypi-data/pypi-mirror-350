import numpy as np
import itertools
from scipy.spatial import cKDTree

class PeriodicCKDTree(cKDTree):
    """
    cKDTree subclass supporting periodic boundary conditions.

    Behaviors:
      - Orthorhombic box (1D bounds) with full periodicity: uses native cKDTree methods.
      - General box (2D bounds matrix): uses query tiling to implement PBC.
    """
    def __init__(self, bounds, data, leafsize=10, pbc=None, force_orth:bool=False):
        data = np.asarray(data, float)
        d    = data.shape[1]

        # Normalize pbc
        if pbc is None:
            pbc = (True,) * d
        elif len(pbc) != d:
            raise ValueError(f"pbc must have length {d}")
        self.pbc = tuple(pbc)

        # Force float-array form
        bounds = np.asarray(bounds, float)
        is_orth = force_orth and ((bounds.ndim==1 and bounds.size==d) \
                  or (bounds.ndim==2 and bounds.shape==(d,d) \
                      and not np.any(np.abs(bounds[~np.eye(d, dtype=bool)])>1e-12)))
      
        if is_orth and all(self.pbc):
            # Orthorhombic periodic box: use native cKDTree periodic support
            box = bounds if bounds.ndim == 1 else np.diag(bounds)
            super().__init__(data, leafsize=leafsize, boxsize=box)
            self._use_native = True
            self.bounds = np.diag(box)
        else:
            # General case: build plain cKDTree on data (no tiling)
            super().__init__(data, leafsize=leafsize)
            self._use_native = False
            if bounds.ndim == 1:
                self.bounds = np.diag(bounds)
            elif bounds.ndim == 2 and bounds.shape == (d, d):
                self.bounds = bounds
            else:
                raise ValueError(f"bounds must be length-{d} or {d}x{d} matrix")

        self._n_orig = data.shape[0]

    def _make_shifts(self, r):
        # Compute integer shifts needed to cover radius r
        lengths = np.linalg.norm(self.bounds, axis=0)
        max_shifts = np.ceil(r / lengths).astype(int)
        axes = [range(-m, m + 1) if p else (0,)
                for m, p in zip(max_shifts, self.pbc)]
        return np.array(list(itertools.product(*axes)), int)

    def query(self, x, k=1, eps=0, p=2, distance_upper_bound=np.inf):
        if self._use_native:
            return super().query(x, k=k, eps=eps, p=p, distance_upper_bound=distance_upper_bound)
        dists, idxs = super().query(x, k=k, eps=eps, p=p, distance_upper_bound=distance_upper_bound)
        return dists, np.mod(idxs, self._n_orig)

    def query_ball_point(self, x, r, p=2., eps=0):
        if self._use_native:
            return super().query_ball_point(x, r, p, eps)

        x_arr = np.asarray(x, float)
        single = (x_arr.ndim == 1)
        Q = x_arr.reshape(-1, x_arr.shape[-1])

        shifts_i = self._make_shifts(r)
        shifts_r = shifts_i.dot(self.bounds)
        tiled = (Q[:, None, :] + shifts_r[None, :, :]).reshape(-1, Q.shape[1])
        raw = super().query_ball_point(tiled, r, p, eps)

        raw = np.array(raw, object).reshape(Q.shape[0], -1)
        out = []
        for row in raw:
            idxs = np.concatenate(row) % self._n_orig
            out.append(np.unique(idxs).tolist())
        return out[0] if single else out

    def query_ball_tree(self, other, r, p=2., eps=0):
        if self._use_native and getattr(other, '_use_native', False):
            return super().query_ball_tree(other, r, p, eps)
        if not isinstance(other, PeriodicCKDTree):
            raise ValueError("Other tree must be PeriodicCKDTree")
        return other.query_ball_point(self.data, r, p, eps)

    def query_pairs(self, r, p=2., eps=0):
        if self._use_native:
            return super().query_pairs(r, p, eps)
        pairs = set()
        neighbors = self.query_ball_point(self.data, r, p, eps)
        for i, nbrs in enumerate(neighbors):
            for j in nbrs:
                if i < j:
                    pairs.add((i, j))
        return sorted(pairs)

    def count_neighbors(self, other, r, p=2.):
        '''
        if self._use_native and getattr(other, '_use_native', False):
            return super().count_neighbors(other, r, p)
        if not isinstance(other, PeriodicCKDTree):
            raise ValueError("Other tree must be PeriodicCKDTree")
        raw = super().count_neighbors(other, r, p)
        return np.array(raw).reshape(-1, self._n_orig).sum(axis=0)
        '''
        if self._use_native and getattr(other, '_use_native', False):
            return super().count_neighbors(other, r, p)
        if not isinstance(other, PeriodicCKDTree):
            raise ValueError("Other tree must be PeriodicCKDTree")

        counts = np.zeros(other.n, dtype=int)
        for i, point in enumerate(other.data):
            indices = self.query_ball_point(point, r, p)
            counts[i] = len(indices)
            
        return counts

    def sparse_distance_matrix(self, other, max_distance, p=2.):
        if self._use_native and getattr(other, '_use_native', False):
            return super().sparse_distance_matrix(other, max_distance, p)
        if not isinstance(other, PeriodicCKDTree):
            raise ValueError("Other tree must be PeriodicCKDTree")
        raw = super().sparse_distance_matrix(other, max_distance, p)
        result = {}
        for (i_t, j_t), dist in raw.items():
            i, j = i_t % self._n_orig, j_t % other._n_orig
            key = (i, j) if i < j else (j, i)
            if key not in result or dist < result[key]:
                result[key] = dist
        return result
