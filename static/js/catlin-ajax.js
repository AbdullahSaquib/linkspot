function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i=0; i<cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length+1));
        break;
      }
    }
  }
  return cookieValue;
}
function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
var csrftoken = getCookie('csrftoken');

function toggleHideShowID(hs_id) {
  var x = document.getElementById(hs_id);
  if(x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function nestedCommentsHtml(username, ncid, content, likes, dislikes) {
  var nchtml =
  "<h5 class='nested-comment-heading'>"+ username +"</h5>" +
  "<p class='nested-comment-content'>"+ content +"</p>" +
  "<strong class='nested-comment-likes' id='like_comment_count"+ncid+"'>"+ likes + "</strong>" +
  " <button class='like_comment' id='like_comment"+ncid+"' data-commentid="+ncid+"  type='button'>" +
    "Like </button> " +
  "<strong class='nested-comment-dislikes' id='dislike_comment_count"+ncid+"'>"+ dislikes + "</strong>" +
  " <button class='dislike_comment' id='dislike_comment"+ncid+"' data-commentid="+ncid+"  type='button'>" +
    " Dislike</button>";
  return nchtml;
}

function mainCommentHtml(id, content, username, last_modified, like_count, dislike_count) {
  var mchtml = "<div class='comment"+id+"'>" +
    "<h5>"+username+" Just Now</h5>"+
    "<p>"+content+"</p>"+
    "<p>"+
    "<strong id='like_comment_count"+id+"'>"+like_count+"</strong> "+
    "<button class='like_comment' id='like_comment"+id+"' data-commentid='"+id+"' type='button'>"+
    "Like"+
    "</button> "+
    "<strong id='dislike_comment_count"+id+"'>"+dislike_count+"</strong> "+
    "<button class='dislike_comment' id='dislike_comment"+id+"' data-commentid='"+id+"' type='button'>"+
    "Dislike"+
    "</button>"+
    "</p>"+
    "<!-- QUERIED NESTED COMMENTS -->"+
    "<button class='see-comment-reply-btn' data-commentid='"+id+"' type='button'>Reply</button>"+
    "<button id='see-replies-btn"+id+"' class='see-replies-btn' type='button' data-mcommentid="+id+">0 Replies</button>"+
    "<form action='' method='post' class='post-comment-reply' id='form-post-comment-reply"+id+"' style='margin-left:30px; display:none;'>"+
    "<p>"+
        "<label for='new-comment"+id+"'>Content:</label>"+
        "<textarea name='content' cols='40' rows='10' placeholder='Post your thoughts' required='' id='new-comment"+id+"'></textarea>"+
        "</p>"+
      "<input class='comment-reply-btn' type='submit' name='PostComment' value='Post' data-commentid='"+id+"'>"+
    "</form>"+
    "<div class='nested-comments' id='div_see_replies"+id+"' style='margin-left:30px; display:none;'></div>"+
    "</div>";
  return mchtml;
}

function post_comment() {
  console.log('Post comment is working');
  var catid = $('#comment-btn').attr('data-catid');
  var comment;
  $.ajax({
    url : '/linkgroup/add-comment/',
    type: 'post',
    data: {
      comment_content:$('#new-comment').val(),
      category_id:catid,
      type:'M',
    },
    success: function(json) {
      $('#new-comment').val('');
      comment = json;
      $('#comments').prepend(mainCommentHtml(json.id, json.content, json.username, json.last_modified, json.like_count, json.dislike_count));
      console.log(comment);
      console.log('Comment posted successfully!');
    },
    error: function(xhr,errmsg,err) {
      alert('Encountered error: '+errmsg);
      console.log(xhr.status + xhr.responseText);
    }
  });
  $('#new-comment').val('');
}

function post_nested_comment(commentid) {
  var catid = $('#comments').attr('data-catid');
  var content = $('#new-comment'+commentid).val();
  console.log('Received(cat-id:'+catid+', comment-id: '+commentid+'): '+content);
  $.ajax({
    url : '/linkgroup/add-comment/',
    type: 'post',
    data: {
      category_id:catid,
      comment_id:commentid,
      comment_content:content,
      type:'N',
    },
    success: function(json) {
      $('#new-comment'+commentid).val('');
      // username, ncid, content, likes, dislikes
      $('#see-replies-btn'+commentid).html(json.parent_comment_count+' Replies');
      $('#div_see_replies'+commentid).prepend(nestedCommentsHtml(json.username, json.id, json.content, json.like_count, json.dislike_count));
      console.log(json);
      console.log('Comment posted successfully!');
    },
    error: function(xhr,errmsg,err) {
      alert('Encountered error: '+errmsg);
      console.log(xhr.status + xhr.responseText);
    }
  });
  $('#new-comment'+commentid).val('');
}

$(document).ready( function() {
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    $("#likes").click( function(event) {
        var catid = $(this).attr('data-catid');
        $.post('/linkgroup/like_category/', {entity_id : catid, liketype:'L'}, function(data){
          $('#like_counts').html(data.likes);
          $('#dislike_counts').html(data.dislikes);
        });
    });

    $("#dislikes").click( function(event) {
        var catid = $(this).attr('data-catid');
        $.ajax({
          url:'/linkgroup/like_category/',
          type: 'post',
          data: {
            entity_id:catid,
            liketype:'D'
          },
          datatype:'json',
          success : function(data){
            $('#like_counts').html(data.likes);
            $('#dislike_counts').html(data.dislikes);
          }
       });
    });

    $(".like_page").click( function(event) {
        var pageid = $(this).attr('data-pageid');
        lpc_id_name = "#like_page_count"+pageid;
        dlpc_id_name = "#dislike_page_count"+pageid;
        $.post('/linkgroup/like_page/', {entity_id : pageid, liketype:'L'}, function(data){
          $(lpc_id_name).html(data.likes);
          $(dlpc_id_name).html(data.dislikes);
        });
    });

    $(".dislike_page").click( function(event) {
        var pageid = $(this).attr('data-pageid');
        lpc_id_name = "#like_page_count"+pageid;
        dlpc_id_name = "#dislike_page_count"+pageid;
        $.post('/linkgroup/like_page/', {entity_id : pageid, liketype:'D'}, function(data){
          $(lpc_id_name).html(data.likes);
          $(dlpc_id_name).html(data.dislikes);
        });
    });

    // $(".like_comment").click( function(event) {
    //     var commentid = $(this).attr('data-commentid');
    //     lcc_id_name = "#like_comment_count"+commentid;
    //     dlcc_id_name = "#dislike_comment_count"+commentid;
    //     $.post('/linkgroup/like_comment/', {entity_id : commentid, liketype:'L'}, function(data){
    //       $(lcc_id_name).html(data.likes);
    //       $(dlcc_id_name).html(data.dislikes);
    //     });
    // });
    //
    // $(".dislike_comment").click( function(event) {
    //     var commentid = $(this).attr('data-commentid');
    //     lcc_id_name = "#like_comment_count"+commentid;
    //     dlcc_id_name = "#dislike_comment_count"+commentid;
    //     $.post('/linkgroup/like_comment/', {entity_id : commentid, liketype:'D'}, function(data){
    //       $(lcc_id_name).html(data.likes);
    //       $(dlcc_id_name).html(data.dislikes);
    //     });
    // });

    $("#comments").on('click', '.see-replies-btn',function(event) {
    // $(".see_replies").on('click', function(event) {
    // $(".see_replies").click( function(event) {
      var mcommentid = $(this).attr('data-mcommentid');
      toggleHideShowID("div_see_replies"+mcommentid);
      if ($("#div_see_replies"+mcommentid).html() === '') {
       $.ajax({
         url:'/linkgroup/see_replies/',
         type: 'get',
         data: {
           main_comment_id : mcommentid
         },
         datatype:'json',
         success : function(data){
           var i;
           for (i=0; i<data.nc_ids.length; i++) {
             $("#div_see_replies"+mcommentid).append(nestedCommentsHtml(
               username=data.usernames[i],
               ncid=data.nc_ids[i],
               content=data.contents[i],
               likes=data.likes[i],
               dislikes=data.dislikes[i]
             ));
           }
         }
       });
     }
    });

    $("#comments").on('click', '.see-comment-reply-btn',function(event) {
      var mcommentid = $(this).attr('data-commentid');
      toggleHideShowID("form-post-comment-reply"+mcommentid);
    });



    // $(".nested-comments").on('click', '.like_comment', function() {
    //       var commentid = $(this).attr('data-commentid');
    //       lcc_id_name = "#like_comment_count"+commentid;
    //       dlcc_id_name = "#dislike_comment_count"+commentid;
    //       $.post('/linkgroup/like_comment/', {entity_id : commentid, liketype:'L'}, function(data){
    //         $(lcc_id_name).html(data.likes);
    //         $(dlcc_id_name).html(data.dislikes);
    //       });
    // });
    //
    // $(".nested-comments").on('click', '.dislike_comment', function() {
    //       var commentid = $(this).attr('data-commentid');
    //       lcc_id_name = "#like_comment_count"+commentid;
    //       dlcc_id_name = "#dislike_comment_count"+commentid;
    //       $.post('/linkgroup/like_comment/', {entity_id : commentid, liketype:'D'}, function(data){
    //         $(lcc_id_name).html(data.likes);
    //         $(dlcc_id_name).html(data.dislikes);
    //       });
    // });

    $("#comments").on('click', '.like_comment', function() {
          var commentid = $(this).attr('data-commentid');
          lcc_id_name = "#like_comment_count"+commentid;
          dlcc_id_name = "#dislike_comment_count"+commentid;
          $.post('/linkgroup/like_comment/', {entity_id : commentid, liketype:'L'}, function(data){
            $(lcc_id_name).html(data.likes);
            $(dlcc_id_name).html(data.dislikes);
          });
    });

    $("#comments").on('click', '.dislike_comment', function() {
          var commentid = $(this).attr('data-commentid');
          lcc_id_name = "#like_comment_count"+commentid;
          dlcc_id_name = "#dislike_comment_count"+commentid;
          $.post('/linkgroup/like_comment/', {entity_id : commentid, liketype:'D'}, function(data){
            $(lcc_id_name).html(data.likes);
            $(dlcc_id_name).html(data.dislikes);
          });
    });

    $("#post-comment-form").on('submit', function(event) {
      event.preventDefault();
      post_comment();
    });

    $("#comments").on('click', '.comment-reply-btn', function(event) {
      event.preventDefault();
      console.log('nested comments is being posted.')
      var commentid = $(this).attr('data-commentid');
      post_nested_comment(commentid);
    });
});
