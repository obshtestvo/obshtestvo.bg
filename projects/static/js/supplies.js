$('.askBtn').on('click', function() {
    userId = invitee = $(this).data('id');
    $.ajax({
        type: "GET",
        url: "?userId=" + userId,
        success: function(data) {
            if (data.length) {
                $('#userSkills').append("<option selected value=''></option");
                for (var i = 0; i < data.length; i++) {
                    $('#userSkills').append("<option value='" + data[i].skill_id + "'>" + data[i].skill + "</option>");
                };
            }
            $('#msg-user-name').text(data[0].user);
            $('#msg-user-mail').text(data[0].email);
            $('#userSkills').on("change", checkSkillsProjectsFilled);
            $('#project').on('change', checkSkillsProjectsFilled);

            $('form.inviteForm').on('submit', function(e) {
                e.preventDefault();
                $.ajax({
                    url: "invitations/",
                    data: $(this).serialize() + "&invitee=" + invitee,
                    type: "POST",
                    success: function(data) {

                        if (data.message) {
                            //TODO - styling the success message
                            $('.inviteMessage').html(data.message);
                            var msg = $('.invHtml').html();
                            $.magnificPopup.open({
                                items: {
                                    src: '<div class="popup default-popup mfp-with-anim round"> ' + msg + ' </div>'
                                }
                            });
                        } else {
                            //TODO - add some error class for styling the fields
                            console.log(data)
                        }

                    },
                    error: function(data) {
                        console.log(data)
                    },
                });
            });
        },
        error: function() {
            //TODO
            alert("Error1");
        },
    })

    var phtml = $('.askForm').html();
    $.magnificPopup.open({
        items: {
            src: '<div class="popup default-popup mfp-with-anim round"> ' + phtml + ' </div>'
        }
    });


    $("#task").select2({
        containerCssClass: 'project select2',
        allowClear: false,
        disable: "disable",
        multiple: false,
        data: [],
        createSearchChoice: function(term, data) {
            if ($(data).filter(function() {
                return this.text.localeCompare(term) === 0;
            }).length === 0) {
                return {
                    id: term,
                    text: term
                };
            }
        },
    }).select2("disable");


    $('.popup form .focus select').select2({
        containerCssClass: 'project select2',
        dropdownCssClass: 'in-popup in-focus-area',
        allowClear: false,
        placeholder: "Моля изберете от менюто"
    });
});

function checkSkillsProjectsFilled() {
    var userSkillsVal = $('#userSkills').select2("val");
    var projectsVal = $('#project').select2("val");

    var userSkillsText = $("#userSkills").find(":selected").text();
    var projectText = $("#project").find(":selected").text();

    if (userSkillsVal) {
        $("#chosen-activity").text(userSkillsText);
    }

    if (projectsVal) {
        $("#chosen-project").text(projectText);

    }

    if (projectsVal && userSkillsVal) {
        changeSkillProjectFields(userSkillsVal, projectsVal, userSkillsText, projectText);
    }
}

function changeSkillProjectFields(userSkillsVal, projectsVal, userSkillsText, projectText) {

    if (userSkillsVal && projectsVal) {
        $("#chosen-activity").text(userSkillsText);
        $("#chosen-project").text(projectText);

        $("#task").select2("enable");
        $.ajax({
            type: "GET",
            url: "?skillId=" + userSkillsVal + "&projectId=" + projectsVal,
            success: function(data) {
                if (data.length) {
                    instance = $("#task").data('select2')
                    for (var i = 0; i < data.length; i++) {
                        instance.opts.data.push({
                            id: data[i].task_id,
                            text: data[i].name
                        })
                    };
                }
            },
            error: function() {
                //TODO
                alert("Error2");
            },
        })
    }
}