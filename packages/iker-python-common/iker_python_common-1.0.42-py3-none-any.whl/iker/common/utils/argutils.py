import argparse
import dataclasses
import inspect
import typing
from collections.abc import Sequence
from typing import Any

from iker.common.utils.typeutils import is_identical_type

__all__ = [
    "ParserTreeNode",
    "ParserTree",
    "ArgParseSpec",
    "argparse_spec",
    "make_argparse"
]

import sys


class ParserTreeNode(object):
    def __init__(self, command: str, parser: argparse.ArgumentParser):
        self.command = command
        self.parser = parser
        self.subparsers = None
        self.child_nodes: list[ParserTreeNode] = []


def construct_parser_tree(
    root_node: ParserTreeNode,
    command_chain: list[str],
    command_key_prefix: str,
    **kwargs,
) -> list[ParserTreeNode]:
    node_path = [root_node]
    if len(command_chain) == 0:
        return node_path

    node = root_node
    for depth, command in enumerate(command_chain):
        if node.subparsers is None:
            node.subparsers = node.parser.add_subparsers(dest=f"{command_key_prefix}:{depth}")
        for child_node in node.child_nodes:
            if child_node.command == command:
                node = child_node
                break
        else:
            if depth == len(command_chain) - 1:
                child_parser = node.subparsers.add_parser(command, **kwargs)
            else:
                child_parser = node.subparsers.add_parser(command)
            child_node = ParserTreeNode(command, child_parser)
            node.child_nodes.append(child_node)
            node = child_node
        node_path.append(node)

    return node_path


class ParserTree(object):
    def __init__(self, root_parser: argparse.ArgumentParser, command_key_prefix: str = "command"):
        self.root_node = ParserTreeNode("", root_parser)
        self.command_key_prefix = command_key_prefix

    def add_subcommand_parser(self, command_chain: list[str], **kwargs) -> argparse.ArgumentParser:
        *_, last_node = construct_parser_tree(self.root_node, command_chain, self.command_key_prefix, **kwargs)
        return last_node.parser

    def parse_args(self, args: list[str] | None = None) -> tuple[list[str], argparse.Namespace]:
        # Before Python 3.12 the `exit_on_error` attribute does not take effect properly
        # if unknown arguments encountered. We have to employ this workaround
        if sys.version_info < (3, 12):
            if self.root_node.parser.exit_on_error:
                known_args_namespace = self.root_node.parser.parse_args(args)
            else:
                known_args_namespace, unknown_args = self.root_node.parser.parse_known_args(args)
                if len(unknown_args or []) > 0:
                    raise argparse.ArgumentError(None, f"unrecognized arguments '{unknown_args}'")
        else:
            known_args_namespace = self.root_node.parser.parse_args(args)

        command_pairs = []
        namespace = argparse.Namespace()
        for key, value in dict(vars(known_args_namespace)).items():
            if key.startswith(self.command_key_prefix) and value is not None:
                command_pairs.append((key, value))
            else:
                setattr(namespace, key, value)

        return list(command for _, command in sorted(command_pairs)), namespace


@dataclasses.dataclass(frozen=True)
class ArgParseSpec(object):
    flag: str | None = None
    name: str | None = None
    action: str | None = None
    default: Any = None
    type: typing.Type | None = None
    choices: list[Any] | None = None
    required: bool | None = None
    help: str | None = None

    def make_kwargs(self) -> dict[str, Any]:
        kwargs = dict(
            action=self.action,
            default=self.default,
            type=self.type,
            choices=self.choices,
            required=self.required,
            help=self.help,
        )

        return {key: value for key, value in kwargs.items() if value is not None}


argparse_spec = ArgParseSpec


def make_argparse(func, parser: argparse.ArgumentParser = None) -> argparse.ArgumentParser:
    if parser is None:
        parser = argparse.ArgumentParser()

    def is_type_of(a: Any, *bs) -> bool:
        return any(is_identical_type(a, b, strict_optional=False, covariant=True) for b in bs)

    sig = inspect.signature(func)
    for name, param in sig.parameters.items():

        arg_name = f"--{name.replace('_', '-')}"

        if param.annotation is None:
            arg_type = str
        elif is_type_of(param.annotation, str, Sequence[str]):
            arg_type = str
        elif is_type_of(param.annotation, int, Sequence[int]):
            arg_type = int
        elif is_type_of(param.annotation, float, Sequence[float]):
            arg_type = float
        elif is_type_of(param.annotation, bool, Sequence[bool]):
            arg_type = bool
        else:
            arg_type = str

        arg_action = "append" if typing.get_origin(param.annotation) in {list, Sequence} else None
        arg_default = None if param.default is inspect.Parameter.empty else param.default

        if isinstance(arg_default, ArgParseSpec):
            spec = arg_default
            spec = dataclasses.replace(spec,
                                       name=spec.name or arg_name,
                                       type=spec.type if spec.type is not None else arg_type,
                                       action=spec.action if spec.action is not None else arg_action)

            if spec.flag is None:
                parser.add_argument(spec.name, **spec.make_kwargs())
            else:
                parser.add_argument(spec.flag, spec.name, **spec.make_kwargs())

        else:
            parser.add_argument(arg_name,
                                type=arg_type,
                                action=arg_action,
                                required=arg_default is None,
                                default=arg_default)

    return parser
