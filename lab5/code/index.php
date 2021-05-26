<?php
  date_default_timezone_set('Asia/Bangkok');
  echo "HOSTNAME: ".gethostname()."<br>";
  echo "SERVER_ADDR: ".$_SERVER['SERVER_ADDR']."<br>";
  echo "REMOTE_ADDR: ".$_SERVER['REMOTE_ADDR']."<br>";
  echo "SERVER_PORT: ".$_SERVER['SERVER_PORT']."<br>";
  echo "REMOTE_PORT: ".$_SERVER['REMOTE_PORT']."<br>";
  echo "HTTP_HOST: ".$_SERVER['HTTP_HOST']."<br>";
  echo "REQUEST_TIME: ".date('Y-m-d H:i:s',$_SERVER['REQUEST_TIME'])."<br>";
  echo "SERVER_SOFTWARE: ".$_SERVER['SERVER_SOFTWARE']."<br>";
  echo "SERVER_PROTOCOL: ".$_SERVER['SERVER_PROTOCOL']."<br>";
  echo "REQUEST_METHOD: ".$_SERVER['REQUEST_METHOD']."<br>";
  echo "HTTP_USER_AGENT: ".$_SERVER['HTTP_USER_AGENT']."<br>";
?>
