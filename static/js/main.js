
function createTask() {
    var name = $("#name").val();
    var workflow = $("#workflow").val();
    var extra_info = $("#extra-info").val();
    var node_names = $("input[name^=node-name]");
    var node_descriptions = $("input[name^=node-description]");
    // the root node doesn't have a parent, so add an empty one
    var node_parents = [""].concat($("input[name^=node-parent]"));

    var nodelist = [];
    for (var i in node_names) {
        nodelist.push({
            name: node_names[i],
            description: node_descriptions[i],
            parent: node_parents[i]
        }
    }

    $.post( "/task",
            {name: name,
             workflow: workflow,
             extra_info: extra_info,
             nodelist: nodelist},
            function(data) {
                if (data == "success") {
                    location.href = "/tasks";
                } else {
                    location.href = "/task";
                }
            });
}

// the node related functions below should be moved into a workflow specific
// js file.
oneNodeFormHtml = "";
function cacheOneNodeForm() {
    // bit of a hack
    var tempNodeForm = $($("#one-node-form").parent().clone());
    $("#parent-step-div", tempNodeForm).css("display", "");
    $("#remove-node-button-div", tempNodeForm).css("display","")
    oneNodeFormHtml = tempNodeForm.html();
}

function addNodeForm() {
    $("#all-node-form").append(oneNodeFormHtml);
    // if we only have two nodes, the second must depend on the first
    if ($("#all-node-form").children().size() == 2) {
        var rootName = $($("input[name^=node-name]")[0]).val();
        $("input[name^=node-parent]").val(rootName);
    }
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
