% if with_import:
from fixture import DataSet

% endif
class ${table.replace('_', ' ').title().replace(' ', '')}Data(DataSet):
    % for row in rows:
    class ${table}_${loop.index}:
        % for column in columns:
        ${column} = ${repr(row[loop.index])}
        % endfor
    % endfor
