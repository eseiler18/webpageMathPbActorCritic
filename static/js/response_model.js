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
            var content = "The model generate : "
            for (let [i, opt] of Object.entries(response.data["output"])){
              if (i>0){
                content += "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp; <strong>" + opt + "</strong> <br>"
              }
              else{
                content += "<strong>" + opt + "</strong> <br>"
              }
            }
            div_response_model.html(content);
            // ask for true or false aswer
            var answer_ask = $("#ask_answer");
            var ask = "Is the answer correct ? &ensp;&ensp;&ensp;&ensp; ";
            // correct
            ask += "<input type='radio' class='btn-check' name='options-outlined' id='success-outlined' autocomplete='off' value='good' >";
            ask += "<label class='btn btn-outline-success' for='success-outlined'>Correct</label>  &ensp;&ensp;&ensp;&ensp;";
            // wrong
            ask += "<input type='radio' class='btn-check' name='options-outlined' id='danger-outlined' autocomplete='off' value='wrong' >"
            ask += "<label class='btn btn-outline-danger' for='danger-outlined'>Wrong</label>"
            answer_ask.html(ask);

            // remove section
            $("#answer_validity").html("")
            $("#critic").html("")
            $("#active_critic").html("")
            $("#critic_response").html("")
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

  $("#select_data").on('change', function(e){
    display_data = $("#display_data");
    var select_data = $("#select_data").val();
    if (select_data != -1){
      $("#response_model").html("")
      $("#ask_answer").html("")
      $("#answer_validity").html("")
      $("#critic").html("")
      $("#active_critic").html("")
      $("#critic_response").html("")
      axios.post('/display_data', {"display_data": select_data})
        .then(function (response) {
          console.log(response);
          var content = " <strong> " + response.data["label"] + "</strong>"
          display_data.html(content)
        })
      }
  });

// answer button
  function reload_answer_validity(){
    var selected_value = $("input[name='options-outlined']:checked").val();
    var answer_validity = $("#answer_validity");
    var content = ""
    if (selected_value == "good") {
        content = "<strong> Nice the anwser is correct </strong>";
    } else if(selected_value == "wrong"){
        content += "<strong> Do you want to be the critic or rely on the automatic critic ? </strong> &ensp;&ensp;&ensp;&ensp; ";
        // content += "<form id='critic_type'>"
        content += "<div class='form-check form-check-inline'>";
        content += "<input class='form-check-input' type='radio' name='critic_type' id='manual_critic' value='manual'>";
        content += "<label class='form-check-label' for='critic_type'> Manual critic </label></div>";
        content += "<div class='form-check form-check-inline'>";
        content += "<input class='form-check-input' type='radio' name='critic_type' id='automatic_critic' value='automatic'>";
        content += "<label class='form-check-label' for='critic_type'> Automatic critic </label></div>";
        content += "<div class='form-check form-check-inline'>";
        content += "<input class='form-check-input' type='radio' name='critic_type' id='oracle_critic' value='oracle'>";
        content += "<label class='form-check-label' for='critic_type'> Oracle critic </label></div>";
    }
    answer_validity.html(content);
}


$('#ask_answer').change(function(e){
  e.preventDefault();
  reload_answer_validity()
});

function generate_critic(){
  var selected_value = $("input[name='critic_type']:checked").val();
  $("#critic_response").html("")
  var critic = $("#critic");
  var active_critic = $("#active_critic");
  var content = "";
  active_critic.html("<button class='btn btn-primary' id='action_resolve'>Resolve</button>")
  if (selected_value == "manual") {
      content += "<form id='hint'>";
      content += "<label for='hint_input' class='form-label'> Give an hint do the model</label>";
      content += "<input class='form-control' id='hint_input' placeholder='Follow hint template' autocomplete='off'></form>";
  } 
  else if(selected_value == "automatic"){
      axios.post('/callcritic', {"critic_mode": selected_value}).then(function (response) {
        content += "The critic model generate the hint : <strong> " + response.data["output"] + "</strong> </br>";
        critic.html(content);
      })
    .catch(function (error) {
      console.log(error);
    });
  }
  else if(selected_value == "oracle"){
    axios.post('/callcritic', {"critic_mode": selected_value}).then(function (response) {
      content += "Based on the true linear equation <strong>"  + response.data["true_linear_formula"] +"</strong> </br>"
      content += "The oracle hint is : <strong> " + response.data["output"] + "</strong> </br>";
      critic.html(content);
    })
  .catch(function (error) {
    console.log(error);
  });
}
  critic.html(content);
}

$('#answer_validity').change(function(e){
  e.preventDefault();
  generate_critic()
});

$("#active_critic").on('click', function(e) {
  e.preventDefault();
  // recup la critic mode
  var critic_mode = $("input[name='critic_type']:checked").val();
  if (critic_mode == "manual") {
    var hint_input = $("#hint_input").val();
  }
  else{
    var hint_input = "nan"
  }
  //div_response_model.html(content)
  axios.post('/performcritic', {"critic_mode": critic_mode, "hint_input": hint_input}).then(function (response) {
          // disp response of the model
          var critic_response = $("#critic_response");
          var content = "The model with help of the critic generate : "
          for (let [i, opt] of Object.entries(response.data["output"])){
            if (i>0){
              content += "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <strong>" + opt + "</strong> <br>"
            }
            else{
              content += "<strong>" + opt + "</strong> <br>"
            }
          }
          critic_response.html(content);
  })
  .catch(function (error) {
  console.log(error);
  });
});
