window.onload = function () {
    eel.select(table_name)(load_table);
}
function load_table (output) {
    console.log("load_table() called");
    parsed_output = JSON.parse(output);
    string_table = "";
    if (table_name === "cuencas" || table_name === "metodos") {
        if (table_name === "cuencas") {
            table_string = "<tr><th>Id cuenca</th><th>Nombre cuenca</th></tr>";
        }
        else if (table_name === "metodos") {
            table_string = "<tr><th>Id método</th><th>Método de pesca</th></tr>";
        }
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0] , "</td><td>", row[1], "</td></tr>"));
    }
    else if (table_name === "pescas") {
        table_string = "<tr><th>Id pesca</th><th>Id cuenca</th><th>Id método</th><th>Fecha</th><th>Peso total</th></tr>";
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0], "</td><td>", row[1], "</td><td>", row[2], "</td><td>", row[3], "</td><td>", row[4], "</td></tr>"));
    }
    document.getElementById("data").innerHTML = table_string;
}