/**
 */

$(document).ready(function () {
    $(".action-dropdown").hide();
    $('.add-remove-to-report').hide();
    $("#eval-checkBoxes").click(function () {
        $("#eval-list").find(".checkBoxClass").prop('checked', $(this).prop('checked'));
    });

    $("#report-checkBoxes").click(function () {
        $("#report-list").find(".checkBoxClass").prop('checked', $(this).prop('checked'));
    });

    $('#eval-list').find(".checkBoxClass").click(function() {
        if ($(this).is(':checked')) {
            // recommend($(this).val())
            // recommendContentBase($(this).val())

        }

        checkedList = getValueUsingClass('#eval-list');
        if (checkedList.length == 1) {
            $("#eval-action").show();
        };

        if (checkedList.length != 1) {
            $("#eval-action").hide();
        };
        if (checkedList.length > 0) {
            $("#add-to-report").show();

        }
        else {
            console.log('hier')
            $("#add-to-report").hide();
        }
    });
    $('#report-list').find(".checkBoxClass").click(function() {
        // if ($(this).is(':checked')) {
        //     recommend($(this).val())
        //     recommendContentBase($(this).val())
        //
        // }

        checkedList = getValueUsingClass('#report-list');
        if (checkedList.length == 1) {
            $("#report-action").show();
        };

        if (checkedList.length != 1) {
            $("#report-action").hide();
        };
        if (checkedList.length > 0) {
            $("#remove-from-report").show();

        }
        else {
            $("#remove-from-report").hide();
        }
    });

    $('a.popup').click(function(){
        newwindow=window.open($(this).attr('href'),'','height=200,width=150');
        if (window.focus) {newwindow.focus()}
        return false;
    });

});


function getValueUsingClass(id){
    var chkArray = [];
    $(id).find(".checkBoxClass:checked").each(function() {
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
    $('#input-name').hide();
    $('#report').html(html).show();
    $('#edit-name').removeClass('hide');
    // createList(name)
}
function showListname() {
    $('#input-name').show();
    $('#report').hide();
}

function createList(name) {
    url = '/merge/project/newEvalList';
    // $.post(url , {name : name} , function (data){
    //    console.log(data)
    // });
    $.ajax({
        type: 'POST',
        url: url,
        // dataType: dataType,
        async: true,
        data : {csrfmiddlewaretoken:'{{csrf_token}}' },
        success: function (html) {
            console.log(html);
        }
    });
}

// function createList(name) {
//
//
// }

// function evalDetail(e_id) {
//     console.log('In');
//     url = "{% url 'profiles:dashboard:evaluation-detail' e.id %";
//     url = '/users/me/dashboard/project/EvaluationDetail/'+ e_id +'/';
//     console.log(url);
//     $.ajax({
//         type: 'GET',
//         url: url,
//         dataType: 'html',
//         async: true,
//         success: function (html) {
//             $('#e-detail-content').html(html);
//         }
//     });
//
// }
function evalDetail(e_id) {
    url = '/users/me/dashboard/project/EvaluationDetail/'+ e_id +'/';
    console.log('hier');
    $('#e-detail-content').load(url);
    $('#e-detail').modal('show');

}

function addToReport(eval_id) {
    ids = getValueUsingClass('#eval-list');
    url = '/merge/project/'+ eval_id + '/add-evaluation-to-list';
    console.log(ids)
    $.ajax({
        type: 'POST',
        url: url,
        // contentType: 'data',
        data : {ids: [1,2,4] , type: 'info' },
        // success: function (data) {
        //     console.log(data);
        // }
    });
    console.log('finish')
}