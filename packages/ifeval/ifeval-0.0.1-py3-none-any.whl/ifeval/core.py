import ast
import difflib
import libcst as cst
from libcst.metadata import (
    MetadataWrapper,
    PositionProvider,
    ParentNodeProvider,
    CodeRange,
)
from libcst import FlattenSentinel
from typing import List, Tuple, Dict, Optional, Union

import logging

logger = logging.getLogger("ifeval")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s:%(levelname)s %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class _IfCollector(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider, )

    def __init__(self):
        self.ifs: List[Tuple[cst.BaseExpression, CodeRange]] = []

    def visit_If(self, node: cst.If):
        position = self.get_metadata(PositionProvider, node)
        self.ifs.append((node.test, position))


class _IfEvaluator(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (
        PositionProvider,
        ParentNodeProvider,
    )

    def __init__(
        self,
        predicates: Dict[Tuple[cst.BaseExpression, CodeRange], Optional[bool]],
    ):
        self.predicates = predicates

    def leave_If(self, original_node: cst.If,
                 updated_node: cst.If) -> Optional[cst.CSTNode]:
        position = self.get_metadata(PositionProvider, original_node)
        parent = self.get_metadata(ParentNodeProvider, original_node)

        pred_value = self.predicates.get((original_node.test, position))
        logger.info(f"Entering {position}")

        def ret(x):
            if isinstance(parent, cst.If):
                return cst.Else(x)
            else:
                return FlattenSentinel(x)

        if pred_value is True:
            return ret(updated_node.body.body)
        elif pred_value is False and updated_node.orelse:
            if isinstance(updated_node.orelse, cst.Else):
                if isinstance(updated_node.orelse.body, tuple):
                    return ret(updated_node.orelse.body)
                else:
                    return ret(updated_node.orelse.body.body)
            else:
                return cst.RemoveFromParent()
        else:
            return updated_node


class IfEval:

    def __init__(self, source_path: str):
        with open(source_path, "r") as f:
            source_code = f.read()
        self.source_lines = source_code.split('\n')

        self.globals_dict = {"__name__": "__main__"}
        logger.info(f"Executing the code from file {source_path}")
        exec(source_code, self.globals_dict)

        self.source_module = cst.parse_module(source_code)
        wrapper = MetadataWrapper(self.source_module)
        collector = _IfCollector()
        wrapper.visit(collector)

        self.predicates = {}
        for node, pos in collector.ifs:
            line_number = pos.start.line
            value = self._evaluate_predicate(
                node, line_number, self.source_lines[line_number - 1])
            if value is not None:
                self.predicates[node, pos] = value

        transformer = _IfEvaluator(self.predicates)
        self.changed_module = wrapper.visit(transformer)
        self.changed_lines = self.changed_module.code.split('\n')

    def _evaluate_predicate(self, predicate: cst.BaseExpression,
                            line_number: int,
                            source_line: str) -> Optional[bool]:
        try:
            expr_code = self.source_module.code_for_node(predicate)
            compiled = compile(
                expr_code,
                "<string>",
                "eval",
                flags=ast.PyCF_ONLY_AST,
            )
            result = eval(
                compile(compiled, "<string>", "eval"),
                self.globals_dict,
            )
            assert isinstance(result, bool), f"{expr_code} is not a boolean!"
            return result
        except Exception as e:
            logger.warning(f"=== Line #{line_number} ===")
            logger.warning(f"Got an error for {expr_code}: {e}")
            logger.warning(f"In line: {repr(source_line)}")
            return None

    def save_to(self, path: str) -> None:
        """Save the transformed code to a file"""
        with open(path, 'w') as f:
            f.write(self.changed_module.code)

    def print_diff(self) -> None:
        """Print the diff between the original and transformed code"""

        lines = ['Changes after if evaluation:'] + [
            line for line in difflib.unified_diff(self.source_lines,
                                                  self.changed_lines)
        ]
        logger.info('\n'.join(lines))
