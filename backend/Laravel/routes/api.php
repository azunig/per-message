<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\MessageController;

// Rutas de Autenticación
Route::post('register', [AuthController::class, 'register']);
Route::post('login', [AuthController::class, 'login']);

// Rutas Protegidas
Route::middleware('auth:api')->group(function () {
    Route::post('logout', [AuthController::class, 'logout']);
    Route::get('me', [AuthController::class, 'me']);

    // Rutas de Mensajes
    Route::post('messages', [MessageController::class, 'store']);
    Route::get('processes/{process_id}/thread', [MessageController::class, 'getThreadForProcess']);
    Route::delete('messages/{message}', [MessageController::class, 'destroy']);
    // Añade aquí las rutas para show y update si las necesitas
});