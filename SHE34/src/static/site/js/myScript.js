/**
 */

rec_engin = true

$(document).ready(function () {

    // Delete confirmation modal in dashboard
    $('#delModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var url = button.data('url')
        var project_name = button.data('project')
        var modal = $(this)
        modal.find('.project_name').text( project_name );
        modal.find('.modal-footer #deleteButton').attr('href' , url);
    });

    //Modal for principle form
    $('#modal-princip').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var p_title = button.data('title');
        var p_des = button.data('des');
        var p_url = button.data('url');
        var modal = $(this);
        modal.find('#title').attr('value' , p_title)
        modal.find('#description').text(p_des);
        modal.find('#add-princip').attr('action' , p_url);
    });

    //merge button hide
    $(".merge-bar").hide();

    $("#eval-checkBoxes").click(function () {
        $("#eval-list").find(".checkBoxClass").prop('checked', $(this).prop('checked'));
        showActions('#eval-list');
        showActions('.common-action');

    });

    $("#report-checkBoxes").click(function () {
        $("#report-list").find(".checkBoxClass").prop('checked', $(this).prop('checked'));
        showActions('#report-list');
        showActions('.common-action');

    });

    //avtivating javascript for placeRec after ajax load
    $('#output').on("click" ,'.checkBoxClass',function() {
        // if ($(this).is(':checked')) {
        showActions('.common-action');
        // }
    });

    //avtivating javascript for contRec after ajax load
    $('#recContBase').on("click" ,'.checkBoxClass',function() {
        // if ($(this).is(':checked')) {
        showActions('.common-action');
        // }
    });

    $('.common-action').find(".checkBoxClass").click(function() {
        showActions('.common-action');
    });

    //getting recommendation after checking each checkbox
    $('#eval-list').find(".checkBoxClass").click(function() {
        if ($(this).is(':checked') & rec_engin) {
            recommend($(this).val());
            recommendContentBase($(this).val());
        }
        showActions('#eval-list');
    });

    //getting recommendation after checking each checkbox in Merged Evals
    $('#report-list').find(".checkBoxClass").click(function() {
        if ($(this).is(':checked') & rec_engin) {
            recommend($(this).val())
            recommendContentBase($(this).val())
        }
        showActions('#report-list')
    });


    $('a.popup').click(function(){
        newwindow=window.open($(this).attr('href'),'','height=200,width=150');
        if (window.focus) {newwindow.focus()}
        return false;
    });

});

function getValueUsingClass(att){
    var chkArray = [];
    $(att).find(".checkBoxClass:checked").each(function() {
        chkArray.push($(this).val());
    });
    return chkArray;
}

//recommed pace base
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

//recommend content base
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

function evalDetail(e_id) {
    url = '/users/me/dashboard/project/EvaluationDetail/'+ e_id +'/';
    $('#e-detail-content').load(url);
    $('#e-detail').modal('show');

}

// function addToReport(list_id) {
//     ids = getValueUsingClass('#eval-list');
//     url = '/merge/project/'+ list_id + '/add-evaluation-to-list';
//     $.post(url , { csrfmiddlewaretoken: getCookie('csrftoken'), ids:ids });
//     location.reload();
// }
//
// function removeFromReport(list_id) {
//     ids = getValueUsingClass('#report-list');
//     url = '/merge/project/'+ list_id + '/remove-evaluation-from-list';
//     // $.ajax({
//     //     type: 'POST',
//     //     url: url,
//     //     // contentType: 'data',
//     //     data : {ids: ids  , type: 'info' },
//     // });
//     $.post(url , { csrfmiddlewaretoken: getCookie('csrftoken'), ids:ids });
//     location.reload();
// }


/**
 * Function to show possible buttons based on chosen checkboxes
 * @param id : id of a top div of checkboxes
 *
 */
function showActions(id){
    checkedList = getValueUsingClass(id);

    // if(id == '#eval-list') {
    //     if (checkedList.length > 0) {
    //         $("#add-to-report").show();
    //
    //     }
    //     else {
    //         $("#add-to-report").hide();
    //     }
    // }
    // if (id =='#report-list') {
    //     if (checkedList.length > 0) {
    //         $("#remove-from-report").show();
    //
    //     }
    //     else {
    //         $("#remove-from-report").hide();
    //     }
    //
    // }

    if(id == '.common-action'){
        if (checkedList.length > 1) {
            $(".merge-bar").show();
        }
        else{
            $(".merge-bar").hide();
        }
    }
}

//Merging evaluations in merge.html
function merge(project_id){
    ids = getValueUsingClass('.common-action');
    url = '/merge/project/'+ project_id + '/merge_selected_evaluations';
    name = 'DEFAULT TITLE',
    $.post(url ,
        { csrfmiddlewaretoken: getCookie('csrftoken'), ids:ids , name :JSON.stringify(name) },
        function (data) {
            if(data.status == 1){
                open(data.url);
                location.reload();
            }
        });
};

//
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//Recommendation on and off
$('.btn-toggle').click(function () {
    $(this).find('.btn').toggleClass('btn-primary');
    $(this).find('.btn').toggleClass('btn-default');
    if ($(this).find('.btn-primary').html() == 'OFF') {
        rec_engin = false;
    }
    else{
        rec_engin = true;
    };

});

//
// function listname() {
//     name = $('#name-eval-list').val();
//     html = '<h4>'+ name + '</h4>'
//     $('#input-name').hide();
//     $('#report').html(html).show();
//     $('#edit-name').removeClass('hide');
// }
// function showListname() {
//     $('#input-name').show();
//     $('#report').hide();
// }
// function createList(name) {
//     url = '/merge/project/newEvalList';
//     // $.post(url , {name : name} , function (data){
//     //    console.log(data)
//     // });
//     $.ajax({
//         type: 'POST',
//         url: url,
//         // dataType: dataType,
//         async: true,
//         data : {csrfmiddlewaretoken:'{{csrf_token}}' },
//         success: function (html) {
//             console.log(html);
//         }
//     });
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
