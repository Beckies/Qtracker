$(document).ready( function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			dataType:'json',
			beforeSend: function(){
				$('#modal-org').modal('show');
			},
			success: function(data){
				$('#modal-org .modal-content').html(data.html_form);
			}
		});

	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('#org-table tbody').html(data.org_list);
					$('#modal-org').modal('hide');
				} else {
					$('#modal-org  .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}
	
// create Org
$(".show-form").click(ShowForm);
$("#modal-org").on("submit",".create-form",SaveForm);

//update Org
$('#org-table').on("click",".show-form-update",ShowForm);
$('#modal-org').on("submit",".update-form",SaveForm)

//delete Org
$('#org-table').on("click",".show-form-delete",ShowForm);
$('#modal-org').on("submit",".delete-form",SaveForm)

// create location
$(".show-form").click(ShowForm);
$("#modal-org").on("submit",".loc-create-form",SaveForm);

//update location
$('#loc-table').on("click",".loc-show-form-update",ShowForm);
$('#modal-org').on("submit",".loc-update-form",SaveForm)

//delete location
$('#loc-table').on("click",".loc-show-form-delete",ShowForm);
$('#modal-org').on("submit",".loc-delete-form",SaveForm)
});

