"use client";

import { useState, useCallback, useRef } from "react";

const MAX_PHOTOS = 50;
const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/heic"];

interface PhotoFile {
  file: File;
  /** Object URL for thumbnail preview — revoke on cleanup */
  previewUrl: string;
  id: string;
}

interface UsePhotoUploadResult {
  photos: PhotoFile[];
  isDragging: boolean;
  error: string | null;
  addPhotos: (files: FileList | File[]) => void;
  removePhoto: (id: string) => void;
  clearPhotos: () => void;
  /** Bind to the hidden <input type="file"> element */
  fileInputRef: React.RefObject<HTMLInputElement>;
  /** Programmatically open the file picker */
  openFilePicker: () => void;
  /** Drag event handlers — spread onto the drop zone element */
  dragHandlers: {
    onDragEnter: (e: React.DragEvent) => void;
    onDragOver: (e: React.DragEvent) => void;
    onDragLeave: (e: React.DragEvent) => void;
    onDrop: (e: React.DragEvent) => void;
  };
}

export function usePhotoUpload(): UsePhotoUploadResult {
  const [photos, setPhotos] = useState<PhotoFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dragCounterRef = useRef(0); // Track nested drag enter/leave events

  const addPhotos = useCallback((files: FileList | File[]) => {
    const fileArray = Array.from(files);
    setError(null);

    // Filter to accepted types
    const validFiles = fileArray.filter((f) => ACCEPTED_TYPES.includes(f.type));
    const invalidCount = fileArray.length - validFiles.length;
    if (invalidCount > 0) {
      setError(
        `${invalidCount} file${invalidCount > 1 ? "s" : ""} skipped — only JPEG, PNG, WebP, and HEIC are supported.`
      );
    }

    setPhotos((prev) => {
      const remaining = MAX_PHOTOS - prev.length;
      if (remaining <= 0) {
        setError(`Maximum ${MAX_PHOTOS} photos allowed.`);
        return prev;
      }

      const toAdd = validFiles.slice(0, remaining);
      if (validFiles.length > remaining) {
        setError(`Only the first ${remaining} photo${remaining > 1 ? "s" : ""} were added (${MAX_PHOTOS} max).`);
      }

      const newPhotos: PhotoFile[] = toAdd.map((file) => ({
        file,
        previewUrl: URL.createObjectURL(file),
        id: `${file.name}-${file.size}-${Date.now()}-${Math.random()}`,
      }));

      return [...prev, ...newPhotos];
    });
  }, []);

  const removePhoto = useCallback((id: string) => {
    setPhotos((prev) => {
      const target = prev.find((p) => p.id === id);
      if (target) URL.revokeObjectURL(target.previewUrl);
      return prev.filter((p) => p.id !== id);
    });
  }, []);

  const clearPhotos = useCallback(() => {
    setPhotos((prev) => {
      prev.forEach((p) => URL.revokeObjectURL(p.previewUrl));
      return [];
    });
  }, []);

  const openFilePicker = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const dragHandlers = {
    onDragEnter: useCallback((e: React.DragEvent) => {
      e.preventDefault();
      dragCounterRef.current += 1;
      if (dragCounterRef.current === 1) setIsDragging(true);
    }, []),

    onDragOver: useCallback((e: React.DragEvent) => {
      e.preventDefault(); // Required to allow drop
    }, []),

    onDragLeave: useCallback((e: React.DragEvent) => {
      e.preventDefault();
      dragCounterRef.current -= 1;
      if (dragCounterRef.current === 0) setIsDragging(false);
    }, []),

    onDrop: useCallback(
      (e: React.DragEvent) => {
        e.preventDefault();
        dragCounterRef.current = 0;
        setIsDragging(false);
        if (e.dataTransfer.files.length > 0) {
          addPhotos(e.dataTransfer.files);
        }
      },
      [addPhotos]
    ),
  };

  return {
    photos,
    isDragging,
    error,
    addPhotos,
    removePhoto,
    clearPhotos,
    fileInputRef,
    openFilePicker,
    dragHandlers,
  };
}
