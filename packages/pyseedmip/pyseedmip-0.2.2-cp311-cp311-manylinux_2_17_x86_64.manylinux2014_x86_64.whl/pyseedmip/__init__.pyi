from __future__ import annotations
import os as os
from pyseedmip.pyseedmip import Constr
from pyseedmip.pyseedmip import Env
from pyseedmip.pyseedmip import ErrorCode
from pyseedmip.pyseedmip import EventHandler
from pyseedmip.pyseedmip import Exception
from pyseedmip.pyseedmip import License
from pyseedmip.pyseedmip import LinExpr
from pyseedmip.pyseedmip import Model
from pyseedmip.pyseedmip import SolStatus
from pyseedmip.pyseedmip import SolverEvent
from pyseedmip.pyseedmip import Status
from pyseedmip.pyseedmip import TempConstr
from pyseedmip.pyseedmip import VType
from pyseedmip.pyseedmip import Var
import sys as sys
from . import pyseedmip
__all__ = ['BEST_SOL_FOUND', 'BINARY', 'Constr', 'DEFAULT_LB', 'DEFAULT_UB', 'ERROR_BOOL_BOUND_WRONG', 'ERROR_BOUND_WRONG', 'ERROR_INTERUPTED', 'ERROR_INVALID_SENSE', 'ERROR_LINEAR_EXPR_NO_SUCH_NAME', 'ERROR_LINEAR_QUANT_NOT_EQUL', 'ERROR_MODEL_DEL_NO_SUCH_NAME', 'ERROR_NAME_CONFLICT', 'ERROR_NO_SOLUTION_YET', 'ERROR_NO_SUCH_NAME', 'ERROR_NO_SUCH_TYPE', 'ERROR_NO_SUCH_VAR', 'ERROR_OBJ_UNSET', 'ERROR_QUANT_NOT_EQUAL', 'ERROR_READ_MPS_ERR', 'ERROR_REDUND_OPRT', 'ERROR_SET_VAL_OUT_BOUND', 'ERROR_SUCCESS', 'ERROR_VAR_ALREADY_FIXED', 'ERROR_VAR_NOT_IN_MODEL', 'Env', 'ErrorCode', 'EventHandler', 'Exception', 'INITIAL_STATE', 'INTEGER', 'INTERUPTED', 'License', 'LinExpr', 'Model', 'NEW_SOL_FOUND', 'REAL', 'SOLVING_END', 'SOL_FOUND', 'SOL_NOT_FOUND', 'START_SOLVING', 'SolStatus', 'SolverEvent', 'Status', 'TempConstr', 'VType', 'Var', 'errorMessages', 'lib_dir', 'os', 'pyseedmip', 'sys']
BEST_SOL_FOUND: Status  # value = <Status.BEST_SOL_FOUND: 3>
BINARY: VType  # value = <VType.BINARY: 0>
DEFAULT_LB: float = 0.0
DEFAULT_UB: float = 1e+20
ERROR_BOOL_BOUND_WRONG: ErrorCode  # value = <ErrorCode.ERROR_BOOL_BOUND_WRONG: 3>
ERROR_BOUND_WRONG: ErrorCode  # value = <ErrorCode.ERROR_BOUND_WRONG: 1>
ERROR_INTERUPTED: ErrorCode  # value = <ErrorCode.ERROR_INTERUPTED: 16>
ERROR_INVALID_SENSE: ErrorCode  # value = <ErrorCode.ERROR_INVALID_SENSE: 8>
ERROR_LINEAR_EXPR_NO_SUCH_NAME: ErrorCode  # value = <ErrorCode.ERROR_LINEAR_EXPR_NO_SUCH_NAME: 11>
ERROR_LINEAR_QUANT_NOT_EQUL: ErrorCode  # value = <ErrorCode.ERROR_LINEAR_QUANT_NOT_EQUL: 14>
ERROR_MODEL_DEL_NO_SUCH_NAME: ErrorCode  # value = <ErrorCode.ERROR_MODEL_DEL_NO_SUCH_NAME: 12>
ERROR_NAME_CONFLICT: ErrorCode  # value = <ErrorCode.ERROR_NAME_CONFLICT: 2>
ERROR_NO_SOLUTION_YET: ErrorCode  # value = <ErrorCode.ERROR_NO_SOLUTION_YET: 18>
ERROR_NO_SUCH_NAME: ErrorCode  # value = <ErrorCode.ERROR_NO_SUCH_NAME: 4>
ERROR_NO_SUCH_TYPE: ErrorCode  # value = <ErrorCode.ERROR_NO_SUCH_TYPE: 5>
ERROR_NO_SUCH_VAR: ErrorCode  # value = <ErrorCode.ERROR_NO_SUCH_VAR: 6>
ERROR_OBJ_UNSET: ErrorCode  # value = <ErrorCode.ERROR_OBJ_UNSET: 10>
ERROR_QUANT_NOT_EQUAL: ErrorCode  # value = <ErrorCode.ERROR_QUANT_NOT_EQUAL: 7>
ERROR_READ_MPS_ERR: ErrorCode  # value = <ErrorCode.ERROR_READ_MPS_ERR: 15>
ERROR_REDUND_OPRT: ErrorCode  # value = <ErrorCode.ERROR_REDUND_OPRT: 9>
ERROR_SET_VAL_OUT_BOUND: ErrorCode  # value = <ErrorCode.ERROR_SET_VAL_OUT_BOUND: 13>
ERROR_SUCCESS: ErrorCode  # value = <ErrorCode.ERROR_SUCCESS: 0>
ERROR_VAR_ALREADY_FIXED: ErrorCode  # value = <ErrorCode.ERROR_VAR_ALREADY_FIXED: 19>
ERROR_VAR_NOT_IN_MODEL: ErrorCode  # value = <ErrorCode.ERROR_VAR_NOT_IN_MODEL: 17>
INITIAL_STATE: Status  # value = <Status.INITIAL_STATE: 0>
INTEGER: VType  # value = <VType.INTEGER: 1>
INTERUPTED: Status  # value = <Status.INTERUPTED: 4>
NEW_SOL_FOUND: Status  # value = <Status.NEW_SOL_FOUND: 2>
REAL: VType  # value = <VType.REAL: 2>
SOLVING_END: Status  # value = <Status.SOLVING_END: 5>
SOL_FOUND: SolStatus  # value = <SolStatus.SOL_FOUND: 1>
SOL_NOT_FOUND: SolStatus  # value = <SolStatus.SOL_NOT_FOUND: 0>
START_SOLVING: Status  # value = <Status.START_SOLVING: 1>
errorMessages: dict  # value = {<ErrorCode.ERROR_SUCCESS: 0>: 'No error', <ErrorCode.ERROR_BOUND_WRONG: 1>: 'The upper bound cannot be less than the lower bound', <ErrorCode.ERROR_NAME_CONFLICT: 2>: 'The var/constr name must be unique', <ErrorCode.ERROR_BOOL_BOUND_WRONG: 3>: 'Invalid bound for a bool var', <ErrorCode.ERROR_NO_SUCH_NAME: 4>: "The var/constr name doesn't exist", <ErrorCode.ERROR_NO_SUCH_TYPE: 5>: "The var type doesn't exist", <ErrorCode.ERROR_NO_SUCH_VAR: 6>: "The given var doesn't exist", <ErrorCode.ERROR_QUANT_NOT_EQUAL: 7>: 'Cnt must be equal to the array length', <ErrorCode.ERROR_INVALID_SENSE: 8>: '< and > are not allowed', <ErrorCode.ERROR_REDUND_OPRT: 9>: 'There are redundant operators in the linear expression', <ErrorCode.ERROR_OBJ_UNSET: 10>: 'The objective function must be set before optimizing', <ErrorCode.ERROR_LINEAR_EXPR_NO_SUCH_NAME: 11>: 'Cannot access this var in the linear expression', <ErrorCode.ERROR_MODEL_DEL_NO_SUCH_NAME: 12>: 'Cannot delete a var/constr not existing', <ErrorCode.ERROR_SET_VAL_OUT_BOUND: 13>: 'The set value must be in the bound', <ErrorCode.ERROR_LINEAR_QUANT_NOT_EQUL: 14>: 'Cnt must be equal to the number of terms', <ErrorCode.ERROR_INTERUPTED: 16>: 'The computation is interupted', <ErrorCode.ERROR_VAR_NOT_IN_MODEL: 17>: 'At least one var in the cons is not in the model', <ErrorCode.ERROR_NO_SOLUTION_YET: 18>: 'no solution available yet', <ErrorCode.ERROR_VAR_ALREADY_FIXED: 19>: 'The var is already fixed.'}
lib_dir: str = '/home/linjk/.local/anaconda3/envs/test/lib/python3.9/site-packages/pyseedmip/../lib'
