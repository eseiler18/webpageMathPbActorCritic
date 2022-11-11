$("#action_select_data").on('click', function(e) {
    e.preventDefault();
    // recup la selection
    var select_data = $("#select_data").val();
    if (select_data != -1){
        axios.post('/main2', {"select_data": select_data})
          .then(function (response) {
            console.log(response);
            // disp answer of the model
            var div_response_model = $("#response_model");
            div_response_model.html("reponse : " + response.data["output"]);
            // ask for true or false aswer
            var answer_ask = $("#ask_answer");
            var ask = "Is the answer correct ? <br> ";
            // correct
            ask += "<input type='radio' class='btn-check' name='options-outlined' id='success-outlined' autocomplete='off' value='good' >";
            ask += "<label class='btn btn-outline-success' for='success-outlined'>Correct</label>  &ensp;";
            // wrong
            ask += "<input type='radio' class='btn-check' name='options-outlined' id='danger-outlined' autocomplete='off' value='wrong' >"
            ask += "<label class='btn btn-outline-danger' for='danger-outlined'>Wrong</label>"
            answer_ask.html(ask);
          })
          .catch(function (error) {
            console.log(error);
          });
    }
  });

function reload_model_selection(){
  var active_train = $("#active_train").is(":checked");
  var active_test = $("#active_test").is(":checked");
  axios.post('/getdataset', {"active_train": active_train, "active_test": active_test} )
          .then(function (response) {
            var select_data = $("#select_data");
            var options =  "<option value='-1' hidden>Choose a Math problem</option>" ;
            // for (opt of response.data["math_pb"]){
            for (let [i, opt] of Object.entries(response.data["math_pb"])){
              options += "<option value='" + response.data["label"][i] + "'>" +  opt + "</option>";
            }
            select_data.html(options);
          })
          .catch(function (error) {
            console.log(error);
          });
}

  $("#active_train").on('change', function(e) {
    e.preventDefault();
    reload_model_selection();
  });
    

  $("#active_test").on('change', function(e) {
    e.preventDefault();
    reload_model_selection();
  });


// answer button
  function reload_answer_validity(){
    var selected_value = $("input[name='options-outlined']:checked").val();
    var answer_validity = $("#answer_validity");
    var content = ""
    if (selected_value == "good") {
        content = "<h3 class='mb-3'>Nice the anwser is good</h3>";
    } else if(selected_value == "wrong"){
        content += " <label for='hintform' class='form-label'> Wrong answer </label>"
        content += " <input class='form-control' id='hintform' placeholder='Type an hint for the model'>"
    }
    answer_validity.html(content);
}

$('#ask_answer').change(function(e){
    e.preventDefault();
    reload_answer_validity()
  });
