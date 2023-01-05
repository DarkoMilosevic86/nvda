# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Annotations are part of the ARIA spec, used to create relationships between nodes.
For example: comment reply chains, terms with definitions, footnotes.

https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Annotations
"""

from dataclasses import dataclass
from typing import (
	TYPE_CHECKING,
	Iterable,
	List,
	Optional,
)

if TYPE_CHECKING:
	import controlTypes
	from NVDAObjects import NVDAObject


class AnnotationTarget:
	"""
	Structured information of an annotation target.
	For example, the definition of a term.
	"""

	@property
	def role(self) -> "controlTypes.Role":
		raise NotImplementedError

	@property
	def targetObject(self) -> "NVDAObject":
		raise NotImplementedError

	@property
	def summary(self) -> str:
		raise NotImplementedError


class AnnotationOrigin:
	"""
	Structured information of an annotation origin.
	For example, a phrase with a footnote and comments associated with it.
	"""

	def __init__(self, originObj: "NVDAObject"):
		self._originObj: "NVDAObject" = originObj

	def __bool__(self):
		"""Performant implementation required to test for annotations
		"""
		raise NotImplementedError

	@property
	def targets(self) -> Iterable[AnnotationTarget]:
		raise NotImplementedError

	@property
	def roles(self) -> Iterable["controlTypes.Role"]:
		raise NotImplementedError

	@property
	def summaries(self) -> Iterable[str]:
		raise NotImplementedError


@dataclass
class _AnnotationNavigationNode:
	"""Node used in _AnnotationNavigation, for navigating between annotations."""
	_TargetIndex = int  # Type for target index
	origin: "NVDAObject"  # this is the last known location
	indexOfLastReportedSummary: Optional[_TargetIndex] = None  # this would be the next destination


class _AnnotationNavigation:
	"""
	Used to manage navigation of annotations.
	For example, reporting a summary of each comment for an object with multiple comment annotation targets.
	"""
	lastReported: Optional[_AnnotationNavigationNode] = None
	priorOrigins: List["NVDAObject"] = []
