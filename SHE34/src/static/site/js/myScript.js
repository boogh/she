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
        checkedList = getValueUsingClass();
        if (checkedList.length == 1) {
            console.log("one!");
            $("#action").show();
        };

        if (checkedList.length != 1) {
            $("#action").hide();
        };

    });
});
//
// $(document).ready(function () {
// 	/* Get the checkboxes values based on the class attached to each check box */
// 	$("#actionbt").click(function() {
// 	    console.log('clicked 1')
// 	    getValueUsingClass();
//
// 	});
//
// 	// /* Get the checkboxes values based on the parent div id */
// 	// $("#buttonParent").click(function() {
// 	//     getValueUsingParentTag();
// 	// });
// });

function getValueUsingClass(){
    /* declare an checkbox array */
    var chkArray = [];

    /* look for all checkboes that have a class 'chk' attached to it and check if it was checked */
    $(".checkBoxClass:checked").each(function() {
        chkArray.push($(this).val());
        // console.log('clicked')
    });

    /* we join the array separated by the comma */
    // var selected;
    // selected = chkArray.join(',') + ",";

    /* check if there is selected checkboxes, by default the length is 1 as it contains one single comma */
    // if(selected.length > 1){
    // }else{
    //     alert("Please at least one of the checkbox");
    // }
    return chkArray;
    // alert("You have selected " + selected);
}