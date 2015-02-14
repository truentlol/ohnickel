$(document).ready(function(){



    init();

    function init(){
        get_threads();
    }




    function get_threads(){
        $.getJSON('/forum/' + globals.forum_id + '/threads', function(json_data){
            //alert(JSON.stringify(json_data));

            if(json_data['success']){
                $.each(json_data['threads'], function(index, forum_json){
                    render_thread(forum_json);
                });
            }



        });
    }




    function render_thread(forum_json){
        var source = $('#thread_template').html();


        var template = Handlebars.compile(source);
        var generated_html = template(forum_json);

        var $forums = $('#threads');

        //Append the handlebars HTML to users div
        $forums.append(generated_html).hide().fadeIn();
    }





    $(document).on('submit', '#thread_form', function(e){
        e.preventDefault();

        var $form = $(this);

        var csrfmiddlewaretoken = $form.find('input[name="csrfmiddlewaretoken"]').val();

        var thread_name = $form.find('#thread_name_input').val();




        var post_url = '/thread/create/';

        var post_data = {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            thread_name: thread_name,
            forum_id: globals.forum_id
        };



        $.post(
            post_url,
            post_data,
            function(response){

                if(response['success']){
                    //Clear the thread name input
                    $form.find('#thread_name_input').val('');
                    render_thread(response['thread']);
                }else{
                    alert(JSON.stringify(response));
                }
            }, 'json'
        );



    })


});