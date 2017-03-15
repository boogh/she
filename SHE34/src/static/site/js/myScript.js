/**
 * Created by Hammer on 3/13/17.
 */

$(document).ready(function () {
    $("#action").hide();
    $("#checkBoxes").click(function () {
        $(".checkBoxClass").prop('checked', $(this).prop('checked'));
    });
    $(".checkBoxClass").click(function() {
        // console.log('clicked 1')
        if ($(this).is(':checked')) {
            console.log('is checked!')
            recommend($(this).val())

        }

        checkedList = getValueUsingClass();
        if (checkedList.length == 1) {
            $("#action").show();
        };

        if (checkedList.length != 1) {
            $("#action").hide();
        };
    });
});


function getValueUsingClass(){
    var chkArray = [];
    $(".checkBoxClass:checked").each(function() {
        chkArray.push($(this).val());
    });
    return chkArray;
}

function recommend(eval_id){
    var url = '/merge/project/'+ eval_id + '/recommend_ajax';
    console.log(url);
    $.ajax({
        type :'GET',
        url : url,
        dataType:'json',
        async : true ,
        success: function (json) {
            console.log(json['evaluations']);
            // $('#output').html(json.evaluations);
        }
    });
}