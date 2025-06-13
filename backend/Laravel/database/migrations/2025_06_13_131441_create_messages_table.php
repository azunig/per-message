<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::disableForeignKeyConstraints();
        Schema::create('messages', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->unsignedBigInteger('parent_id')->nullable();
            $table->unsignedBigInteger('process_id');
            $table->enum('type', ['comentario', 'solicitud', 'pregunta', 'email'])->default('comentario');
            $table->text('message');
            $table->string('attachment_url', 2048)->nullable();
            $table->boolean('is_deleted')->default(false);
            $table->timestamps();

            $table->foreign('parent_id')->references('id')->on('messages')->onDelete('cascade');
            $table->index('process_id');
        });
        Schema::enableForeignKeyConstraints();
    }

    public function down(): void
    {
        Schema::disableForeignKeyConstraints();
        Schema::dropIfExists('messages');
        Schema::enableForeignKeyConstraints();
    }
};