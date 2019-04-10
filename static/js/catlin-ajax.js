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
  "<div class='article-metadata'>" +
  "<a class='mr-2' href='#'>"+username+"</a></div>" +
  "<p class='nested-comment-content'>"+ content +"</p>" +
  "<strong class='nested-comment-likes' id='like_comment_count"+ncid+"'>"+ likes + "</strong>" +
  " <button class='btn btn-info btn-sm like_comment' id='like_comment"+ncid+"' data-commentid="+ncid+"  type='button'>" +
    "Like </button> " +
  "<strong class=' ml-2 nested-comment-dislikes' id='dislike_comment_count"+ncid+"'>"+ dislikes + "</strong>" +
  " <button class='btn btn-secondary btn-sm dislike_comment' id='dislike_comment"+ncid+"' data-commentid="+ncid+"  type='button'>" +
    " Dislike</button>";
  return nchtml;
}

function mainCommentHtml(id, content, username, last_modified, like_count, dislike_count) {
  var mchtml = "<div class='comment"+id+"'>" +
    "<div class='article-metadata'>"+
    "<a class='mr-2' href='#'>"+username+"</a>"+
    "<small class='text-muted'>Just Now</small></div>"+
    "<p>"+content+"</p>"+
    "<p>"+
    "<strong id='like_comment_count"+id+"'>"+like_count+"</strong> "+
    "<button class='btn btn-info btn-sm like_comment' id='like_comment"+id+"' data-commentid="+id+" type='button'>"+
    "Like"+
    "</button> "+
    "<strong class='ml-2' id='dislike_comment_count"+id+"'>"+dislike_count+"</strong> "+
    "<button class='btn btn-secondary btn-sm dislike_comment' id='dislike_comment"+id+"' data-commentid='"+id+"' type='button'>"+
    "Dislike"+
    "</button>"+
    "</p>"+
    "<!-- QUERIED NESTED COMMENTS -->"+
    "<a class='text-primary see-comment-reply-btn' data-commentid='"+id+"' type='button'>Reply</a>"+
    "<a id='see-replies-btn"+id+"' class='text-primary ml-4 see-replies-btn' type='button' data-mcommentid="+id+">0 Replies</a>"+
    "<div class='post-comment-reply' id='form-post-comment-reply"+id+"' style='margin-left:30px; display:none;'>"+
        "<textarea name='content' placeholder='Post your thoughts' id='new-comment"+id+"' style='width:100%'></textarea>"+
        "<input class='btn btn-outline-info btn-sm comment-reply-btn' type='submit' name='PostComment' value='Post' data-commentid='"+id+"'>"+
    "</div>"+
    "<div class='nested-comments' id='div_see_replies"+id+"' style='margin-left:30px; display:none;'></div>"+
    "</div><br/>";
  return mchtml;
}

function postComment() {
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
      if(json.username) {
        $('#new-comment').val('');
        comment = json;
        $('#comments').prepend(mainCommentHtml(json.id, json.content, json.username, json.last_modified, json.like_count, json.dislike_count));
        console.log(comment);
        console.log('Comment posted successfully!');
      }
    },
    error: function(xhr,errmsg,err) {
      alert('Encountered error: '+errmsg);
      console.log(xhr.status + xhr.responseText);
    }
  });
  $('#new-comment').val('');
}

function postNestedComment(commentid) {
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
      if(json.username) {
        $('#new-comment'+commentid).val('');
        $('#see-replies-btn'+commentid).html(json.parent_comment_count+' Replies');
        $('#div_see_replies'+commentid).prepend(nestedCommentsHtml(json.username, json.id, json.content, json.like_count, json.dislike_count));
        console.log(json);
        console.log('Comment posted successfully!');
      }
    },
    error: function(xhr,errmsg,err) {
      alert('Encountered error: '+errmsg);
      console.log(xhr.status + xhr.responseText);
    }
  });
  $('#new-comment'+commentid).val('');
}

function likeDislikeCategory(parThis, likeType) {
  var catid = $(parThis).attr('data-catid');
  $.post('/linkgroup/like_category/', {entity_id : catid, liketype:likeType}, function(data){
    $('#like_counts').html(data.likes);
    $('#dislike_counts').html(data.dislikes);
  });
}

function likeDislikePageComment(parThis, entity_type, likeType) {
  var pageid = $(parThis).attr("data-"+entity_type+"id");
  lpc_id_name = "#like_"+entity_type+"_count"+pageid;
  dlpc_id_name = "#dislike_"+entity_type+"_count"+pageid;
  $.post("/linkgroup/like_"+entity_type+"/", {entity_id : pageid, liketype: likeType}, function(data){
    $(lpc_id_name).html(data.likes);
    $(dlpc_id_name).html(data.dislikes);
  });
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
        likeDislikeCategory(this, 'L');
    });

    $("#dislikes").click( function(event) {
      likeDislikeCategory(this, 'D');
    });

    $(".like_page").click( function(event) {
      likeDislikePageComment(this, 'page', 'L');
    });

    $(".dislike_page").click( function(event) {
      likeDislikePageComment(this, 'page', 'D');
    });

    $("#comments").on('click', '.like_comment', function () {
        likeDislikePageComment(this,'comment', 'L');
    });

    $("#comments").on('click', '.dislike_comment', function() {
        likeDislikePageComment(this,'comment', 'D');
    });

    $("#comments").on('click', '.see-replies-btn',function(event) {
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

    $("#post-comment-form").on('submit', function(event) {
      event.preventDefault();
      postComment();
    });

    $("#comments").on('click', '.comment-reply-btn', function(event) {
      event.preventDefault();
      console.log('nested comments is being posted.')
      var commentid = $(this).attr('data-commentid');
      postNestedComment(commentid);
    });
});
