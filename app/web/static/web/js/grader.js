$( document ).ready(function() {

    //on load
    var inputTxt = $("#grading_txt").text()
    $.ajax({
            url: '/home/ajax_grader/',
            data: {
              'inputTxt': inputTxt
            },
            dataType: 'json',
            success: function (data) {

              $( "#graded_txt" ).append( data['graded_txt'] )
              $("#grading_results").append(data['grading_results'])
                $( "#progress_bar" ).remove();
                $( "#wait_hint" ).remove();
              $("#color_guide").append(data['color_guide'])
            }
          });


  $( "#graded_txt" ).on( "click", '#jump_to_page_btn', function() {
    var page_number = $('#page_number').val().trim();
    var input_txt =  $('#input_txt').val();
    if(!$.isNumeric(page_number) || page_number == "0"){
        alert('Page number should just be a number starting with 1. e.g. 2');
       }
    else{

      $.ajax({
            url: '/home/ajax_grader/page/',
            data: {
                'page_number':page_number,
              'input_txt': input_txt
            },
            dataType: 'json',
            success: function (data) {
                $( "#graded_txt" ).empty()
                $("#grading_results").empty()
                $("#color_guide").empty()
              $( "#graded_txt" ).append( data['graded_txt'] )
              $("#grading_results").append(data['grading_results'])
                $( "#progress_bar" ).remove();
                $( "#wait_hint" ).remove();
              $("#color_guide").append(data['color_guide'])
            }
          });

    }
  });

});