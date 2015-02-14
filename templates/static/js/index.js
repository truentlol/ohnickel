$(document).ready(function(){



    init();

    function init(){
        get_forums();
    }




    function get_forums(){
        $.getJSON('/forums', function(json_data){
            //alert(JSON.stringify(json_data));

            if(json_data['success']){
                $.each(json_data['forums'], function(index, forum_json){
                    render_forum(forum_json);
                });
            }



        });
    }




    function render_forum(forum_json){
        var source = $('#forum_template').html();


        var template = Handlebars.compile(source);
        var generated_html = template(forum_json);

        var $forums = $('#forums');

        //Append the handlebars HTML to users div
        $forums.append(generated_html).hide().fadeIn();
    }





    $(document).on('submit', '#forum_form', function(e){
        e.preventDefault();

        var $form = $(this);


        var csrfmiddlewaretoken = $form.find('input[name="csrfmiddlewaretoken"]').val();





        var forum_name = $form.find('#forum_name_input').val();
        var forum_description = $form.find('#forum_description_input').val();
        var forum_sticky = false;

        if($form.find('#forum_sticky').is(':checked')){
            //alert('checkbox is checked');
            forum_sticky = true;
        }else{
            //alert('checkbox is not checked');
        }


        var post_url = '/forum/create/';

        var post_data = {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            forum_name: forum_name,
            forum_description: forum_description,
            forum_sticky: forum_sticky
        };



        $.post(
            post_url,
            post_data,
            function(response){
                if(response['success']){
                    render_forum(response['forum']);
                }else{
                    alert(JSON.stringify(response));
                }
            }, 'json'
        );



    })


});