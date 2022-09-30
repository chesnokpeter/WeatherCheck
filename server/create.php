<?php
require 'db.php';
$db = new DataBase();
$db->connect();
$data = file_get_contents("https://raw.githubusercontent.com/pensnarik/russian-cities/master/russian-cities.json");
$city = json_decode($data);
foreach ($city as $c) {
	$city =	trim($c['name']);
	$query = "INSERT INTO city.citys (`id`, `name`) VALUES (NULL, '{$city}');";
	$db->query_not_answer($query);
}
