var send_data = {};
$(document).ready(function () {
    getAPIData();
    getlocations();

    $('#locations').on('change', function () {
        // since province and region is dependent
        if(this.value === "all")
            send_data['location'] = "";
        else
            send_data['location'] = this.value;

        //get province of selected country

        getProvince(this.value);
        // get api data of updated filters

        getAPIData();
    });

    $('#sort_by').on('change', function () {
        send_data['sort_by'] = this.value;
        getAPIData();
    });
});

function getAPIData() {
    let url = $('#list_data').attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
    });
}


function getCountries() {
    // fill the options of countries by making ajax call

    // obtain the url from the countries select input attribute

    let url = $("#locations").attr("url");

    // makes request to getCountries(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            locations_option = "<option value='all' selected>All locations</option>";
            $.each(result["locations"], function (a, b) {
                locations_option += "<option>" + b + "</option>"
            });
            $("#locations").html(locations_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}
