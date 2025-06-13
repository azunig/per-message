echo "############"

echo "artisan optimize:clear: comandos de cache:clear, route:clear, config:clear y view:clear de una sola vez..."
php artisan optimize:clear

echo "############"
echo "############"
echo "############"

echo "artisan config:clear: Borra el caché de configuración. Después de cambiar tu archivo .env"
php artisan config:clear

echo "############"
echo "############"
echo "############"

echo "artisan route:clear: Borra el caché de rutas. Esencial después de añadir o cambiar rutas en api.php o web.php."
php artisan route:clear

echo "############"
echo "############"
echo "############"

echo "artisan view:clear: Borra las vistas de Blade compiladas."
php artisan view:clear

echo "############"
echo "############"
echo "############"

echo "Refrescando el autoloader de Composer..."
composer dump-autoload

echo "############"
echo "############"
echo "############"

echo "Levantando la cosa"
php artisan serve --port=8002

echo "############"
echo "############"
echo "############"

echo "artisan cache:clear: Borra el caché de la aplicación (datos que guardas manualmente en el caché)."
php artisan cache:clear