% if with_import:
from fixture import DataSet

% endif
class ${fixture_class_name}(DataSet):
    % for row in rows:
    class ${table}_${loop.index}:
        % for column in columns:
        ${column} = ${repr(row[loop.index])}
        % endfor
    % endfor
