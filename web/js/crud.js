window.onload = function () {
    eel.select(table_name)(load_table);
}

function write_error (error_msg) {
    alert(error_msg);
    document.location.href = "index.html";
}

function load_table (output) {
    console.log("load_table() called");
    console.log(output)
    parsed_output = JSON.parse(output);

    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERROR]")) {
        write_error(parsed_output);
        return
    }

    string_table = "";
    if (table_name === "cuencas" || table_name === "metodos") {
        if (table_name === "cuencas") {
            table_string = "<thead><tr><th>Id Cuenca</th><th>Cuenca Hidrográfica</th></tr></thead><tbody>";
        }
        else if (table_name === "metodos") {
            table_string = "<thead><tr><th>Id método</th><th>Método de pesca</th></tr></thead><tbody>";
        }
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0] , "</td><td>", row[1], "</td></tr>"));
    }
    else if (table_name === "pescas") {
        table_string = "<thead><tr><th>Id pesca</th><th>Id cuenca</th><th>Id método</th><th>Fecha</th><th>Peso total</th></tr></thead><tbody>";
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0], "</td><td>", row[1], "</td><td>", row[2], "</td><td>", row[3], "</td><td>", row[4], "</td></tr>"));
    }
    table_string = table_string.concat("</tbody>");
    document.getElementById("data").innerHTML = table_string;
}