import numpy as np

from aiohttp import ClientSession, ClientTimeout
from dataclasses import dataclass
from pldag import PLDAG
from typing import Dict, List, Optional
from enum import Enum
from hashlib import md5
from pickle import dumps, loads
from itertools import starmap

class ConnectionError(Exception):
    pass

class SolverType(str, Enum):
    DEFAULT = "default"

@dataclass
class SolutionResponse:

    solution:   Optional[Dict[str, int]]    = None
    error:      Optional[str]               = None
    status:     Optional[str]               = None
    objective:  Optional[float]             = None

@dataclass
class ICache:

    def set(self, key: str, value: bytes):
        pass

    def get(self, key: str):
        pass

@dataclass
class Solver:
    
    url: str

    # Optional cache
    cache_builder:  Optional[ICache] = None
    cache_server:   Optional[ICache] = None

    async def health(self, timeout: int = 3600) -> bool:
        try:
            async with ClientSession(timeout=ClientTimeout(timeout)) as session:
                async with session.get(f"{self.url}/health", timeout=5) as response:
                    return response.status == 200
        except Exception as e:
            # Log exception (optional, useful for debugging)
            print(f"Health check failed: {e}")
            return False
        
    def prepare_model(self, model: PLDAG, assume: dict) -> tuple:
        """Prepare the model to be sent to the server"""

        def model_polyhedron(model: PLDAG, assume: dict) -> tuple:
            A, b = model.to_polyhedron(**assume)
            rows, cols = np.nonzero(A)
            vals = A[rows, cols]
            result = (A.shape[0], A.shape[1], b, rows.tolist(), cols.tolist(), vals.tolist())
            del A, rows, cols, vals
            return result

        if self.cache_builder is not None:
            key = md5(dumps((model.sha1(), assume))).hexdigest()
            cached = self.cache_builder.get(key)
            if cached is not None:
                return loads(cached)
            
            data = model_polyhedron(model, assume)
            self.cache_builder.set(key, dumps(data))
            return data
        
        else:
            return model_polyhedron(model, assume)

    async def solve(
        self, 
        model: PLDAG, 
        objectives: List[Dict[str, int]], 
        assume: Dict[str, complex] = {}, 
        solver: SolverType = SolverType.DEFAULT,
        maximize: bool = True,
        timeout: int = 3600,
    ) -> List[SolutionResponse]:
        
        if self.cache_server is not None:
            key = md5(dumps((model.sha1(), objectives, assume, solver, maximize))).hexdigest()
            cached = self.cache_server.get(key)
            if cached is not None:
                return loads(cached)

        nrows, ncols, b_dense, A_sparse_rows, A_sparse_cols, A_sparse_vals = self.prepare_model(model, assume)
        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            async with session.post(
                f"{self.url}/model/solve-one/linear",
                json={
                    "model": {
                        "polyhedron": {
                            "A": {
                                "rows": A_sparse_rows,
                                "cols": A_sparse_cols,
                                "vals": A_sparse_vals,
                                "shape": {"nrows": nrows, "ncols": ncols}
                            },
                            "b": b_dense.tolist(),
                            "variables": list(
                                starmap(
                                    lambda k, i: {
                                        "id": k,
                                        "bound": [
                                            int(model._dvec[i].real), 
                                            int(model._dvec[i].imag)
                                        ],
                                    },
                                    model._imap.items()
                                )
                            )
                        },
                        "columns": model.columns.tolist(),
                        "intvars": model.integer_primitives.tolist()
                    },
                    "direction": "maximize" if maximize else "minimize",
                    "objectives": objectives,
                    "solver": solver.value
                },
                headers={
                    "Content-Type": "application/json"
                }
            ) as response:
                
                # Free memory
                # del A_sparse_rows, A_sparse_cols, A_sparse_vals

                if response.status != 200:
                    data = await response.json()
                    error = data.get('error', {})
                    if error.get('code') == 400:
                        raise ValueError(error.get('message', 'Unknown input error'))
                    else:
                        raise Exception(error.get('message', 'Unknown error'))
                
                else:
                    # Process the response
                    data = await response.json()
                    result = list(
                        map(
                            lambda x: SolutionResponse(**x),
                            data.get("solutions", [])
                        )
                    )

                    # Cache the result if a cache server is available
                    if self.cache_server is not None:
                        self.cache_server.set(key, dumps(result))
                    
                    return result
