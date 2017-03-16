/**
 * Created by Hammer on 3/13/17.
 */

$(document).ready(function () {
    $("#action").hide();
    $('.addToReport').hide();
    $("#checkBoxes").click(function () {
        $("#eval-list").find(".checkBoxClass").prop('checked', $(this).prop('checked'));
    });
    $(".checkBoxClass").click(function() {
        // console.log('clicked 1')
        if ($(this).is(':checked')) {
            recommend($(this).val())
            recommendContentBase($(this).val())

        }

        checkedList = getValueUsingClass();
        if (checkedList.length == 1) {
            $("#action").show();
        };

        if (checkedList.length != 1) {
            $("#action").hide();
        };
        if (checkedList.length > 0) {
            $(".addToReport").show();

        }
        else {
            console.log('hier')
            $(".addToReport").hide();
        }
    });
    $('a.popup').click(function(){
		newwindow=window.open($(this).attr('href'),'','height=200,width=150');
		if (window.focus) {newwindow.focus()}
		return false;
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
    $.ajax({
        type :'GET',
        url : url,
        dataType:'html',
        async : true ,
        success: function(html) {
            $('#output').html(html);
        }
    });
}


function recommendContentBase(eval_id) {
    var url = '/merge/project/' + eval_id + '/recommend';
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'html',
        async: true,
        success: function (html) {
            $('#recContBase').html(html);
        }
    });
}

function listname() {
    name = $('#name-eval-list').val();
    html = '<h4>'+ name + '</h4>'
    $('#input-name').hide()
    $('#report').html(html);
    $('#edit-name').removeClass('hide');
}