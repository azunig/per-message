<?php
namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class MessageResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'message' => $this->is_deleted ? 'Este mensaje ha sido eliminado.' : $this->message,
            'type' => $this->type,
            'user_id' => $this->user_id, // Añadimos el user_id
            'process_id' => $this->process_id,
            'parent_id' => $this->parent_id,
            'is_deleted' => (bool) $this->is_deleted,
            'attachment_url' => $this->attachment_url,
            'created_at' => $this->created_at->toDateTimeString(),
            'children' => MessageResource::collection($this->whenLoaded('children')),
        ];
    }
}