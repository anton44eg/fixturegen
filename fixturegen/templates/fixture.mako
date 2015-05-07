% if with_import:
from fixture import DataSet

% endif
class ${fixture_class_name}(DataSet):
    % for row in rows:
    class ${row_class_name(row)}:
        % for column in columns:
        ${column} = ${repr(row[loop.index])}
        % endfor
    % endfor
