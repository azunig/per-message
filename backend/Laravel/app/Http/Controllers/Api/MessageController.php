<?php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Message;
use App\Http\Resources\MessageResource;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class MessageController extends Controller
{
    #public function __construct()
    #{
    #    $this->middleware('auth:api');
    #}

    public function store(Request $request): MessageResource
    {
        $validatedData = $request->validate([
            'parent_id' => 'nullable|exists:messages,id',
            'process_id' => 'required|integer',
            'message' => 'required|string',
            'type' => 'required|in:comentario,solicitud,pregunta,email',
            'attachment_url' => 'nullable|string|max:2048',
        ]);

        $validatedData['user_id'] = auth('api')->id();
        $message = Message::create($validatedData);
        return new MessageResource($message);
    }

    public function getThreadForProcess(int $processId): JsonResponse
    {
        $rootMessages = Message::where('process_id', $processId)
                               ->whereNull('parent_id')
                               ->with('childrenRecursive')
                               ->latest()
                               ->get();
        return response()->json(MessageResource::collection($rootMessages));
    }

    // Los métodos show, update, destroy también deben ser implementados como antes,
    // pero añadiendo una comprobación de autorización. Ejemplo:
    public function destroy(Message $message): JsonResponse
    {
        // Comprueba si el usuario autenticado es el dueño del mensaje
        if (auth('api')->id() !== $message->user_id) {
            return response()->json(['error' => 'Unauthorized'], 403);
        }

        $message->is_deleted = true;
        $message->save();

        return response()->json(null, 204);
    }
}