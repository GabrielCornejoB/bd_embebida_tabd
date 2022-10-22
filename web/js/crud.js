function update_table () {
    console.log("update_table() called");
    eel.select(table_name)(load_table);
}

window.onload = function () {
    eel.select(table_name)(load_table);
    if (table_name === "pescas") {
        eel.select("metodos")(load_select_met);
        eel.select("cuencas")(load_select_cue);
    }
}

function load_select_met (output) {
    parsed_output = JSON.parse(output);
    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERROR]")) {
        write_error(parsed_output);
        return
    }
    const zeroPad = (num, places) => String(num).padStart(places, '0');
    select_string = "<option disabled selected value style'color:#cfcfcf59'>---</option>";
    parsed_output.forEach(row => select_string = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - ", row[1], "</option>"));
    document.getElementById("create_arg_2").innerHTML = select_string;
    document.getElementById("update_arg_2").innerHTML = select_string;
}
function load_select_cue (output) {
    parsed_output = JSON.parse(output);
    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERROR]")) {
        write_error(parsed_output);
        return
    }
    const zeroPad = (num, places) => String(num).padStart(places, '0');
    select_string = "<option disabled selected value style'color:#cfcfcf59'>---</option>";
    parsed_output.forEach(row => select_string = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - ", row[1], "</option>"));
    document.getElementById("create_arg_1").innerHTML = select_string;
    document.getElementById("update_arg_1").innerHTML = select_string;
}

// READ
function load_table (output) {
    console.log("READ");
    parsed_output = JSON.parse(output);

    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERROR]")) {
        write_error(parsed_output);
        return
    }

    table_string = "";
    select_string = "<option disabled selected value style='color:#cfcfcf59'>---</option>";
    const zeroPad = (num, places) => String(num).padStart(places, '0');
    if (table_name === "cuencas" || table_name === "metodos") {
        if (table_name === "cuencas") {
            table_string = "<thead><tr><th>Id Cuenca</th><th>Cuenca Hidrográfica</th></tr></thead><tbody>";
        }
        else if (table_name === "metodos") {
            table_string = "<thead><tr><th>Id método</th><th>Método de pesca</th></tr></thead><tbody>";
        }
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0] , "</td><td>", row[1], "</td></tr>"));
        parsed_output.forEach(row => select_string  = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - ", row[1], "</option>"));
    }
    else if (table_name === "pescas") {
        table_string = "<thead><tr><th>Id pesca</th><th>Id cuenca</th><th>Id método</th><th>Fecha</th><th>Peso total</th></tr></thead><tbody>";
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0], "</td><td>", row[1], "</td><td>", row[2], "</td><td>", row[3], "</td><td>", row[4], "</td></tr>"));
        parsed_output.forEach(row => select_string = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - (", row[1], ", ", row[2], ", ", row[3], ", ", row[4], ")</option>"));
    }
    table_string = table_string.concat("</tbody>");
    document.getElementById("data").innerHTML = table_string;
    document.getElementById("update_select").innerHTML = select_string;
    document.getElementById("delete_select").innerHTML = select_string;
}

//CREATE
document.querySelector(".crud_create").onclick = function() {
    l_args = []
    create_arg_1 = document.getElementById("create_arg_1").value;
    l_args.push(create_arg_1);

    if (table_name === "pescas") {
        create_arg_2 = document.getElementById("create_arg_2").value;
        create_arg_3 = document.getElementById("create_arg_3").value;
        create_arg_4 = document.getElementById("create_arg_4").value;
        l_args.push(create_arg_2);
        l_args.push(create_arg_3);
        l_args.push(create_arg_4);
    }
    eel.create(table_name, l_args)(add_register);    
}
function add_register(output) {
    console.log("CREATE");
    clean_fields();
    parsed_output = JSON.parse(output);
    if (parsed_output.startsWith("[ERROR]")) {
        write_error(parsed_output);
        return
    }
    else if (parsed_output.startsWith("[MSG]")) {
        write_msg(parsed_output);
        update_table();
    }
}

// UPDATE
document.querySelector(".crud_update").onclick = function() {
    update_arg_1 = document.getElementById("update_arg_1").value;
    update_arg_2 = document.getElementById("update_select").value;
    eel.update(table_name, [update_arg_1, update_arg_2])(update_register);
}
function update_register(output) {
    console.log("UPDATE");
    clean_fields();
    parsed_output = JSON.parse(output);
    if (parsed_output.startsWith("[ERROR]")) {
        write_error(parsed_output);
        return
    }
    else if (parsed_output.startsWith("[MSG]")) {
        write_msg(parsed_output);
        update_table();
    }
}

// DELETE
document.querySelector(".crud_delete").onclick = function() {
    delete_arg_1 = document.getElementById("delete_select").value;
    eel.delete(table_name, delete_arg_1)(delete_register);
}
function delete_register(output) {
    console.log("DELETE");
    clean_fields();
    parsed_output = JSON.parse(output);
    if (parsed_output.startsWith("[ERROR")) {
        write_error(parsed_output);
        return
    }
    else if (parsed_output.startsWith("[MSG]")) {
        write_msg(parsed_output);
        update_table();
    }
}