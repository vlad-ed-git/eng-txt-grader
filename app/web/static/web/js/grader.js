$( document ).ready(function() {

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

});