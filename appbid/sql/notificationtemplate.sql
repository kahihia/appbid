insert into notification_notificationtemplate(`name`,`language`,`type`,`subject`,`template`,`description`,`version`,`create_time`,`last_modify`,`modifier_id`)
values('register-active',1,1,'The active account email for register from AppsWalk','Hi {username},\n\r Please click the blow link to active your account \n\r {active_link}','active account email','1.0',now(),now(),1);