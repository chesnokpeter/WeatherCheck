<?php
require 'db.php';
$db = new DataBase();
$db->connect();
$q = mb_strtolower($_GET['q']);
$l = $_GET["limit"];
$query = "SELECT * FROM city.citys WHERE LOWER(name) LIKE('{$q}%') LIMIT {$l};";
$result = $db->query_answer($query);
echo json_encode($result);
