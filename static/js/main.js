
function createTask() {
    name = $("#name").val();
    workflow = $("#workflow").val();
    extra_info = $("#extra-info").val();
    $.post( "/task",
            {name: name,
             workflow: workflow,
             extra_info: extra_info},
            function(data) {
                if (data == "success") {
                    location.href = "/tasks";
                } else {
                    location.href = "/task";
                }
            });
}


// adapted from
// http://stackoverflow.com/questions/5180382/convert-json-data-to-a-html-table
function buildHtmlTable(myList, table_id, rowFunction) {
    //var columns = addAllColumnHeaders(myList, table_id);

    for (var i = 0 ; i < myList.length ; i++) {
        var row = $('<tr/>');
        row = rowFunction(myList[i], row);
        $(table_id).append(row);
    }
}

function defaultRowFunction(myRowData, row, columns) {
    for (var colIndex = 0 ; colIndex < columns.length ; colIndex++) {
        var cellValue = myRowData[columns[colIndex]];

        if (cellValue == null) {
            cellValue = "";
        }

        row.append($('<td/>').html(cellValue));
    }
    return row;
}

function addAllColumnHeaders(myList, table_id) {
    var columnSet = [];
    var headerTr = $('<tr/>');

    for (var i = 0 ; i < myList.length ; i++) {
        var rowHash = myList[i];
        for (var key in rowHash) {
            if ($.inArray(key, columnSet) == -1){
                columnSet.push(key);
                headerTr.append($('<th/>').html(key));
            }
        }
    }
    $(table_id).append(headerTr);

    return columnSet;
}

// generates a callback function to be passed to
// $.getJson(..)
function jsonToTableGenerator(table_id, rowFunction) {
    return function(data, textStatus, jqXHR) {
        buildHtmlTable(data, table_id, rowFunction);
    }
}
