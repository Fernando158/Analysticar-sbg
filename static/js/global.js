
/* global ConversationPanel: true, PayloadPanel: true*/
/* eslint no-unused-vars: "off" */

// Other JS files required to be loaded first: apis.js, conversation.js, payload.js
var firstClick = true;

$('.chat-button').click(function(){
      // Initialize all modules
      if (firstClick){
      	ConversationPanel.init();
	  	PayloadPanel.init();	
	  	firstClick = false;
      }
	  
 });