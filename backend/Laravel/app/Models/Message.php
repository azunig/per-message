<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Message extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id', 'parent_id', 'process_id', 'type', 'message', 'attachment_url',
    ];

    public function user(): BelongsTo { return $this->belongsTo(User::class); }
    public function parent(): BelongsTo { return $this->belongsTo(Message::class, 'parent_id'); }
    public function children(): HasMany { return $this->hasMany(Message::class, 'parent_id'); }
    public function childrenRecursive(): HasMany { return $this->children()->with('childrenRecursive'); }
}