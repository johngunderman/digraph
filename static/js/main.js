
function createTask() {
    name = $("#name")[0].value
    workflow = $("#workflow")[0].value
    extra_info = $("#extra-info")[0].value
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
