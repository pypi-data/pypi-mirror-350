"""The module that defines the ``PlagiarismCase`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..utils import to_dict
from .user import User
from .work import Work


@dataclass
class PlagiarismCase:
    """This class represents a single plagiarism case.

    A case is a combination of two submissions that look alike, and a single
    case contains multiple matches.
    """

    #: The id of this case.
    id: "int"
    #: The two users that are in this case.
    users: "t.Sequence[User]"
    #: The maximum match. This N% of the parsable lines in one of the two
    #: submissions is part of a match.
    match_max: "float"
    #: Same as `match_max` but this is the average of the two submissions.
    match_avg: "float"
    #: The submissions in this match.
    submissions: "t.Optional[t.Sequence[Work]]"
    #: Can you see more detail about this match?
    can_see_details: "bool"
    #: The assignment ids of this match.
    assignment_ids: "t.Sequence[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this case.",
            ),
            rqa.RequiredArgument(
                "users",
                rqa.List(parsers.ParserFor.make(User)),
                doc="The two users that are in this case.",
            ),
            rqa.RequiredArgument(
                "match_max",
                rqa.SimpleValue.float,
                doc="The maximum match. This N% of the parsable lines in one of the two submissions is part of a match.",
            ),
            rqa.RequiredArgument(
                "match_avg",
                rqa.SimpleValue.float,
                doc="Same as `match_max` but this is the average of the two submissions.",
            ),
            rqa.RequiredArgument(
                "submissions",
                rqa.Nullable(rqa.List(parsers.ParserFor.make(Work))),
                doc="The submissions in this match.",
            ),
            rqa.RequiredArgument(
                "can_see_details",
                rqa.SimpleValue.bool,
                doc="Can you see more detail about this match?",
            ),
            rqa.RequiredArgument(
                "assignment_ids",
                rqa.List(rqa.SimpleValue.int),
                doc="The assignment ids of this match.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "id": to_dict(self.id),
            "users": to_dict(self.users),
            "match_max": to_dict(self.match_max),
            "match_avg": to_dict(self.match_avg),
            "submissions": to_dict(self.submissions),
            "can_see_details": to_dict(self.can_see_details),
            "assignment_ids": to_dict(self.assignment_ids),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["PlagiarismCase"], d: t.Dict[str, t.Any]
    ) -> "PlagiarismCase":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            users=parsed.users,
            match_max=parsed.match_max,
            match_avg=parsed.match_avg,
            submissions=parsed.submissions,
            can_see_details=parsed.can_see_details,
            assignment_ids=parsed.assignment_ids,
        )
        res.raw_data = d
        return res
