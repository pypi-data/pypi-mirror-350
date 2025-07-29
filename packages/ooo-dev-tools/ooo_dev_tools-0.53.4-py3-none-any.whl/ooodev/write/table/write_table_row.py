from __future__ import annotations
from typing import Any, TYPE_CHECKING, Generator, Tuple

from ooodev.mock import mock_g
from ooodev.adapter.beans.property_change_implement import PropertyChangeImplement
from ooodev.adapter.beans.vetoable_change_implement import VetoableChangeImplement
from ooodev.adapter.text.text_table_row_comp import TextTableRowComp
from ooodev.events.partial.events_partial import EventsPartial
from ooodev.format.inner.style_partial import StylePartial
from ooodev.utils import gen_util as mGenUtil
from ooodev.utils.data_type.cell_obj import CellObj
from ooodev.utils.data_type.range_obj import RangeObj
from ooodev.utils.data_type.range_values import RangeValues
from ooodev.utils.partial.lo_inst_props_partial import LoInstPropsPartial
from ooodev.utils.partial.prop_partial import PropPartial
from ooodev.write.partial.write_doc_prop_partial import WriteDocPropPartial
from ooodev.write.table.partial.write_table_prop_partial import WriteTablePropPartial

if TYPE_CHECKING:
    from com.sun.star.text import TextTableRow  # service
    from ooodev.write.table.write_table_cell import WriteTableCell
    from ooodev.write.table.write_table_cell_range import WriteTableCellRange
    from ooodev.write.style.direct.table.row_styler import RowStyler


class WriteTableRow(
    WriteDocPropPartial,
    WriteTablePropPartial,
    EventsPartial,
    TextTableRowComp,
    LoInstPropsPartial,
    PropertyChangeImplement,
    VetoableChangeImplement,
    PropPartial,
    StylePartial,
):
    """Represents writer table row."""

    def __init__(self, owner: Any, component: TextTableRow, idx: int = -1) -> None:
        """
        Constructor

        Args:
            owner (Any): Owner of this component.
            component (TextTableRow): UNO object that supports ``om.sun.star.text.TextTableRow`` service.
            idx (int, optional): Index of this row. Defaults to ``-1``.
        """
        if not isinstance(owner, WriteTablePropPartial):
            raise ValueError("owner must be a WriteTablePropPartial instance.")
        WriteDocPropPartial.__init__(self, obj=owner.write_doc)  # type: ignore
        WriteTablePropPartial.__init__(self, obj=owner.write_table)
        EventsPartial.__init__(self)
        LoInstPropsPartial.__init__(self, lo_inst=owner.write_table.lo_inst)
        TextTableRowComp.__init__(self, component=component)  # type: ignore
        # pylint: disable=no-member
        generic_args = self._ComponentBase__get_generic_args()  # type: ignore
        PropertyChangeImplement.__init__(self, component=self.component, trigger_args=generic_args)
        VetoableChangeImplement.__init__(self, component=self.component, trigger_args=generic_args)
        PropPartial.__init__(self, component=component, lo_inst=self.lo_inst)
        StylePartial.__init__(self, component=component)

        self._style_direct_row = None
        self._owner = owner
        self._index = idx
        self._range_obj = None

    def __getitem__(self, key: Any) -> WriteTableCell:
        """
        Returns the Write Table Cell. The cell must exist in the current row.

        Args:
            key (Any): Key. can be a integer such as ``2`` for column index (``-1`` get last cell in row, ``-2`` second last) or a string such as "A1" or a ``CellObj``.

        Returns:
            WriteTableCell: Table Cell Object.

        Raises:
            IndexError: If the key is out of range.

        Note:
            If key is an integer then it is assumed to be a column index.
            If key is a string then it is assumed to be a cell name.

            Cell names and ``CellObj`` are relative to the current row.
            If the current row is the first row of the table then the cell names and ``CellObj`` are the same as the parent table.
            If the row index is 3 then ``row[`A1`]`` is the same as ``table[`A4`]``.

            No mater the row index the first cell of the row is always ``row[0]`` or ``row['A1']``.

        Example:
            .. code-block:: python

                >>> table = doc.tables[0]
                >>> row = table.rows[3]
                >>> cell = row["A1"] # or row[0]
                >>> print(cell, cell.value)
                WriteTableCell(cell_name=A4) Goldfinger
        """
        if isinstance(key, int):
            vals = self._get_range_values()
            index = self._get_index(key)
            cell_obj = CellObj.from_idx(col_idx=index, row_idx=vals.row_start, sheet_idx=vals.sheet_idx)
            if cell_obj not in self.range_obj:
                raise IndexError(f"Index {key} is out of range.")
            return self.write_table[cell_obj]

        cell_range = self.get_cell_range()
        return cell_range[key]

    def __iter__(self) -> Generator[WriteTableCell, None, None]:
        """Iterates through the cells of the row."""
        if self._index < 0:
            raise IndexError("Index is not set.")
        for cell_obj in self.range_obj:
            yield self.write_table[cell_obj]

    def __repr__(self) -> str:
        if self._index < 0:
            return f"WriteTableRow(index={self.index})"
        return f"WriteTableRow(index={self.index}, range={self.range_obj})"

    def get_cell_range(self) -> WriteTableCellRange:
        """Gets the range of this row."""
        return self.write_table.get_cell_range(self.range_obj)

    def _get_index(self, idx: int, allow_greater: bool = False) -> int:
        """
        Gets the index.

        Args:
            idx (int): Index of sheet. Can be a negative value to index from the end of the list.
            allow_greater (bool, optional): If True and index is greater then the number of
                sheets then the index becomes the next index if sheet were appended. Defaults to False.

        Returns:
            int: Index value.
        """
        count = self.range_obj.row_count
        return mGenUtil.Util.get_index(idx, count, allow_greater)

    def _get_range_values(self) -> RangeValues:
        """Gets the range values of this row."""
        col_start = 0
        col_end = len(self.write_table.columns) - 1
        row_start = self.index
        row_end = self.index

        return RangeValues(col_start=col_start, col_end=col_end, row_start=row_start, row_end=row_end, sheet_idx=-2)

    def get_row_data(self, as_floats: bool = False) -> Tuple[float | str | None, ...]:
        """
        Gets the data of the row.

        Args:
            as_floats (bool, optional): If ``True`` then get all values as floats. If the cell is not a number then it is converted to ``0.0``. Defaults to ``False``.

        Returns:
            Tuple[float | str | None, ...]: Row data. If ``as_floats`` is ``True`` then all values are floats.
        """

        cell_range = self.write_table.get_cell_range(self.range_obj)
        return cell_range.get_row_data(idx=0, as_floats=as_floats)

    @property
    def owner(self) -> Any:
        """Owner of this component."""
        return self._owner

    @property
    def style_direct(self) -> RowStyler:
        """
        Direct Cell Styler.

        Returns:
            CellStyler: Character Styler
        """
        if self._style_direct_row is None:
            # pylint: disable=import-outside-toplevel
            from ooodev.write.style.direct.table.row_styler import RowStyler

            self._style_direct_row = RowStyler(owner=self.write_table, component=self.component)
            self._style_direct_row.add_event_observers(self.event_observer)
        return self._style_direct_row

    @property
    def index(self) -> int:
        """Index of this row."""
        return self._index

    @property
    def range_obj(self) -> RangeObj:
        """
        Range Object that represents this row cell range.
        """
        if self._range_obj is None:
            if self._index < 0:
                raise IndexError("Index is not set.")
            self._range_obj = RangeObj.from_range(self._get_range_values())
        return self._range_obj


if mock_g.FULL_IMPORT:
    from ooodev.write.style.direct.table.row_styler import RowStyler
