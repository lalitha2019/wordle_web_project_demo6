const year_select_element = document.getElementById("year_select");
const month_select_element = document.getElementById("month_select");

let title_string = "Counts for all answers";

function show_tab(index) {
    // Retrieve tab content elements
    const tab_contents =
        document.getElementsByClassName("tab-content");

    // Loop through all tab content elements
    for (const tab of tab_contents) {
    
        // Remove the "active" class from all tab content elements
        tab.classList.remove("active");
    }
    
    // Add the "active" class to the tab 
    // content element at the specified index
    tab_contents[index].classList.add("active");
}

function populate_options(select_element, options_list) {
    // Clear existing dynamic options (keeping the placeholder index 0)
	select_element.length = 1;

    //loop through options_list
    options_list.forEach(option_val => {
 	const option = document.createElement("option");

    // Assign value and text content
 	option.value = option_val
	option.textContent = option_val;

    // Append the option to the dropdown list
	select_element.appendChild(option);
    });
}
  
document.addEventListener("DOMContentLoaded", 
    function() {
        const year_data = document.getElementById('year_vals_div').dataset.year_vals;
        const year_vals = JSON.parse(year_data);
        populate_options(year_select_element, year_vals)
       
        //populate months only after a year is selected
        
    })

year_select_element.addEventListener("change",
    function() {
        const selected_year = year_select_element.value
        const month_data = document.getElementById('month_vals_div').dataset.month_vals;
        const month_vals = JSON.parse(month_data);
        const today = new Date()

        if(selected_year == '2021') {
            populate_options(month_select_element, month_vals.slice(5,))
        }
        else if (selected_year == today.getFullYear()){
            populate_options(month_select_element, month_vals.slice(0, today.getMonth()+1))
        }
        else {
            populate_options(month_select_element, month_vals)
        }
    })

function show_vals() {
    const data_to_send = {'year': year_select_element.value,
                                'month': month_select_element.value};
    
    if (year_select_element.value != ""){
        if (month_select_element.value != "") {
            title_string = "Counts for " + year_select_element.value + " " +  month_select_element.value
        } else {title_string = "Counts for " + year_select_element.value}
    } else { title_string = "Counts for all answers"}

    fetch('/api/show_selected', {
        method: 'POST',
        headers: {
                    'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_to_send)
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Success');

        document.getElementById('counts_header').innerHTML = title_string;
        document.getElementById('show_table').innerHTML =  data.table;
        show_tab(1)

        document.getElementById('graph_header').innerHTML = title_string
        document.getElementById('graph').src='data:image/png;base64,' + data.graph;
        })
        .catch(error => console.error('Error sending data: ', error));
    }

function show_position_graph(position_name) {
    const data_to_send = {'position_name': position_name};
        fetch('/api/get_position', {
            method: 'POST',
            headers: {
                        'Content-Type': 'application/json'
            },
            body: JSON.stringify(data_to_send)
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success');
            //const title_string = "Counts for " + year_select_element.value + " " + month_select_element.value;
            document.getElementById('graph_header').innerHTML = title_string + ' in ' + position_name + ' place';
            document.getElementById('graph').src='data:image/png;base64,' + data.graph;
            show_tab(2);
            //alert(data.position)
        })
        .catch(error => console.error('Error sending data: ', error));
        //window.location.href='graph_counts'
    }

    function show_letter_graph(letter_name) {
        const data_to_send = {'letter_name': letter_name};
            fetch('/api/get_letter', {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json'
                },
                body: JSON.stringify(data_to_send)
            })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success');
                //const title_string = "Counts for " + year_select_element.value + " " + month_select_element.value;
                document.getElementById('graph_header').innerHTML = title_string + ' for ' + letter_name;
                document.getElementById('graph').src='data:image/png;base64,' + data.graph
                show_tab(2)
                //alert(data.letter)
            })
            .catch(error => console.error('Error sending data: ', error));
            //window.location.href='graph_counts'
    }

            