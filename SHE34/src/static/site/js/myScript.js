/**
 * Created by Hammer on 3/13/17.
 */

$(document).ready(function () {
    $("#checkBoxes").click(function () {
        $(".checkBoxClass").prop('checked', $(this).prop('checked'));
        // $(".checkBoxClass").attr('checked', true);
        // $(".checkBoxClass").prop('checked', false);


        console.log('bla');
    });
});