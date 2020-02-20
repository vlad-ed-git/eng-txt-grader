$( document ).ready(function() {

    //on load
    var inputTxt = $("#grading_txt").text()
    $.ajax({
            url: '/ajax_grader/',
            data: {
              'inputTxt': inputTxt
            },
            dataType: 'json',
            success: function (data) {

              $( "#graded_txt" ).append( data['graded_txt'] )
              $("#grading_results").append(data['grading_output_html'])
                $( "#progress_bar" ).remove();
                $( "#wait_hint" ).remove();
              $("#color_guide").append(data['color_guide'])
            }
          });



    //toggle grades
   $( "#color_guide" ).on( "click", '.gradeBtns', function() {
        toggleClass = '.' + this.id;
        $(toggleClass).toggle()
   });



});