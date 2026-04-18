"use client";

import { useState, useCallback } from "react";
import { Pencil, X, Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { formatListPrice } from "@/lib/utils";
import type { PropertyDetails } from "@/types";

interface PropertyDetailsCardProps {
  property: PropertyDetails;
  mode: "edit" | "readonly";
  /** Called with the updated property when agent edits a field (edit mode only) */
  onChange?: (updated: PropertyDetails) => void;
  className?: string;
}

// Fact rows to display in the grid
const FACT_KEYS: Array<{
  label: string;
  key: keyof PropertyDetails;
  format?: (v: unknown) => string;
}> = [
  { label: "Year Built",     key: "yearBuilt" },
  { label: "Lot Size",       key: "lotSize" },
  { label: "Garage",         key: "garage" },
  { label: "Property Type",  key: "propertyType" },
  { label: "MLS #",          key: "mlsNumber" },
];

export function PropertyDetailsCard({
  property,
  mode,
  onChange,
  className,
}: PropertyDetailsCardProps) {
  // Track which fact field is currently being edited
  const [editingKey, setEditingKey] = useState<keyof PropertyDetails | null>(null);
  const [newFeatureText, setNewFeatureText] = useState("");
  const [isAddingFeature, setIsAddingFeature] = useState(false);

  const isEditable = mode === "edit";

  const handleFieldChange = useCallback(
    (key: keyof PropertyDetails, value: string | number) => {
      if (!onChange) return;
      onChange({ ...property, [key]: value });
    },
    [property, onChange]
  );

  const handleRemoveFeature = useCallback(
    (feature: string) => {
      if (!onChange) return;
      onChange({
        ...property,
        keyFeatures: property.keyFeatures.filter((f) => f !== feature),
      });
    },
    [property, onChange]
  );

  const handleAddFeature = useCallback(() => {
    const trimmed = newFeatureText.trim();
    if (!trimmed || !onChange) return;
    onChange({
      ...property,
      keyFeatures: [...property.keyFeatures, trimmed],
    });
    setNewFeatureText("");
    setIsAddingFeature(false);
  }, [newFeatureText, property, onChange]);

  return (
    <div className={cn("rounded-lg border border-border overflow-hidden", className)}>
      {/* Card header */}
      <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-3">
        <span className="section-label">Property Details</span>
        {isEditable && (
          <span className="flex items-center gap-1 text-[11px] text-muted-foreground">
            <Pencil className="h-3 w-3" />
            Tap any field to edit
          </span>
        )}
      </div>

      {/* Address block — edit mode only */}
      {isEditable && (
        <div className="border-b border-border px-4 py-3">
        {isEditable && editingKey === "address" ? (
          <input
            autoFocus
            className="mb-1 w-full rounded-md border border-border bg-background px-2 py-1 text-sm font-semibold text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            value={property.address}
            onChange={(e) => handleFieldChange("address", e.target.value)}
            onBlur={() => setEditingKey(null)}
            onKeyDown={(e) => e.key === "Enter" && setEditingKey(null)}
          />
        ) : (
          <p
            className={cn(
              "mb-1 text-sm font-semibold text-foreground",
              isEditable && "cursor-pointer hover:text-foreground/80"
            )}
            onClick={() => isEditable && setEditingKey("address")}
          >
            {property.address || "Tap to add address"}
          </p>
        )}

        {/* City / State / Zip — editable inline */}
        <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
          {isEditable && editingKey === "city" ? (
            <input autoFocus className="w-24 rounded border border-border bg-background px-1.5 py-0.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
              value={property.city} onChange={(e) => handleFieldChange("city", e.target.value)}
              onBlur={() => setEditingKey(null)} onKeyDown={(e) => e.key === "Enter" && setEditingKey(null)} />
          ) : (
            <span className={cn(isEditable && "cursor-pointer hover:text-foreground")}
              onClick={() => isEditable && setEditingKey("city")}>{property.city || "City"}</span>
          )}
          <span>,</span>
          {isEditable && editingKey === "state" ? (
            <input autoFocus className="w-10 rounded border border-border bg-background px-1.5 py-0.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
              value={property.state} onChange={(e) => handleFieldChange("state", e.target.value)}
              onBlur={() => setEditingKey(null)} onKeyDown={(e) => e.key === "Enter" && setEditingKey(null)} />
          ) : (
            <span className={cn(isEditable && "cursor-pointer hover:text-foreground")}
              onClick={() => isEditable && setEditingKey("state")}>{property.state || "ST"}</span>
          )}
          {isEditable && editingKey === "zip" ? (
            <input autoFocus className="w-16 rounded border border-border bg-background px-1.5 py-0.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
              value={property.zip} onChange={(e) => handleFieldChange("zip", e.target.value)}
              onBlur={() => setEditingKey(null)} onKeyDown={(e) => e.key === "Enter" && setEditingKey(null)} />
          ) : (
            <span className={cn(isEditable && "cursor-pointer hover:text-foreground")}
              onClick={() => isEditable && setEditingKey("zip")}>{property.zip || "Zip"}</span>
          )}
        </div>
      </div>
      )}

      {/* Price + stats row — edit mode only */}
      {isEditable && (
      <div className="flex items-center gap-4 border-b border-border px-4 py-3">
        {isEditable && editingKey === "listPrice" ? (
          <input autoFocus className="w-32 rounded-md border border-border bg-background px-2 py-1 text-base font-semibold text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            value={property.listPrice || ""}
            onChange={(e) => handleFieldChange("listPrice", Number(e.target.value.replace(/\D/g, "")))}
            onBlur={() => setEditingKey(null)} onKeyDown={(e) => e.key === "Enter" && setEditingKey(null)} />
        ) : (
          <span className={cn("text-base font-semibold text-foreground", isEditable && "cursor-pointer hover:text-foreground/80")}
            onClick={() => isEditable && setEditingKey("listPrice")}>
            {formatListPrice(property.listPrice)}
          </span>
        )}
        <div className="h-5 w-px bg-border" />
        <EditableStatItem value={String(property.beds)} label="Beds" fieldKey="beds"
          isEditable={isEditable} editingKey={editingKey} setEditingKey={setEditingKey}
          onChange={(v: string) => handleFieldChange("beds", Number(v))} />
        <div className="h-5 w-px bg-border" />
        <EditableStatItem value={String(property.baths)} label="Baths" fieldKey="baths"
          isEditable={isEditable} editingKey={editingKey} setEditingKey={setEditingKey}
          onChange={(v: string) => handleFieldChange("baths", Number(v))} />
        <div className="h-5 w-px bg-border" />
        <EditableStatItem value={property.sqft > 0 ? property.sqft.toLocaleString() : "—"} label="Sqft" fieldKey="sqft"
          isEditable={isEditable} editingKey={editingKey} setEditingKey={setEditingKey}
          onChange={(v: string) => handleFieldChange("sqft", Number(v.replace(/,/g, "")))} />
      </div>
      )}

      {/* Facts grid */}
      <div className="grid grid-cols-2 border-b border-border">
        {FACT_KEYS.map(({ label, key }) => {
          const rawValue = property[key];
          const displayValue = rawValue != null ? String(rawValue) : "—";
          const isEditingThis = editingKey === key;

          return (
            <div
              key={key}
              className="flex items-center justify-between border-b border-muted px-4 py-2.5 last:border-b-0 [&:nth-last-child(-n+2)]:border-b-0"
            >
              <span className="text-[11px] text-muted-foreground">{label}</span>
              {isEditable && isEditingThis ? (
                <input
                  autoFocus
                  className="w-24 rounded-md border border-border bg-background px-2 py-0.5 text-right text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                  value={displayValue === "—" ? "" : displayValue}
                  onChange={(e) => handleFieldChange(key, e.target.value)}
                  onBlur={() => setEditingKey(null)}
                  onKeyDown={(e) => e.key === "Enter" && setEditingKey(null)}
                />
              ) : (
                <span
                  className={cn(
                    "text-xs font-medium text-foreground",
                    isEditable && "cursor-pointer rounded px-1 hover:bg-muted transition-colors"
                  )}
                  onClick={() => isEditable && setEditingKey(key)}
                >
                  {displayValue}
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* Key features chips */}
      <div className="px-4 py-3">
        <p className="mb-2 text-[11px] text-muted-foreground">Key features</p>
        <div className="flex flex-wrap gap-1.5">
          {property.keyFeatures.map((feature) => (
            <span
              key={feature}
              className="flex items-center gap-1.5 rounded-full border border-border bg-muted/50 py-1 pl-3 pr-2 text-xs text-foreground"
            >
              {feature}
              {isEditable && (
                <button
                  onClick={() => handleRemoveFeature(feature)}
                  className="flex h-4 w-4 items-center justify-center rounded-full text-muted-foreground hover:bg-border hover:text-foreground transition-colors"
                  aria-label={`Remove ${feature}`}
                >
                  <X className="h-2.5 w-2.5" />
                </button>
              )}
            </span>
          ))}

          {/* Add chip — edit mode only */}
          {isEditable && (
            isAddingFeature ? (
              <input
                autoFocus
                className="h-[30px] rounded-full border border-dashed border-border bg-transparent px-3 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                placeholder="Add feature…"
                value={newFeatureText}
                onChange={(e) => setNewFeatureText(e.target.value)}
                onBlur={() => {
                  handleAddFeature();
                  setIsAddingFeature(false);
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleAddFeature();
                  if (e.key === "Escape") {
                    setNewFeatureText("");
                    setIsAddingFeature(false);
                  }
                }}
              />
            ) : (
              <button
                onClick={() => setIsAddingFeature(true)}
                className="flex h-[30px] items-center gap-1 rounded-full border border-dashed border-border bg-transparent px-3 text-xs text-muted-foreground hover:border-foreground hover:text-foreground transition-colors"
              >
                <Plus className="h-3 w-3" />
              </button>
            )
          )}
        </div>
      </div>
    </div>
  );
}

// ── Internal sub-component ────────────────────────────────────────

function StatItem({ value, label }: { value: string; label: string }) {
  return (
    <div className="flex flex-col items-start gap-0.5">
      <span className="text-sm font-semibold text-foreground leading-none">{value}</span>
      <span className="text-[10px] text-muted-foreground leading-none">{label}</span>
    </div>
  );
}

function EditableStatItem({
  value, label, fieldKey, isEditable, editingKey, setEditingKey, onChange,
}: {
  value: string;
  label: string;
  fieldKey: keyof PropertyDetails;
  isEditable: boolean;
  editingKey: keyof PropertyDetails | null;
  setEditingKey: (k: keyof PropertyDetails | null) => void;
  onChange: (v: string) => void;
}) {
  if (isEditable && editingKey === fieldKey) {
    return (
      <div className="flex flex-col items-start gap-0.5">
        <input autoFocus
          className="w-16 rounded border border-border bg-background px-1.5 py-0.5 text-sm font-semibold text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          defaultValue={value === "—" ? "" : value}
          onChange={(e) => onChange(e.target.value)}
          onBlur={() => setEditingKey(null)}
          onKeyDown={(e) => e.key === "Enter" && setEditingKey(null)} />
        <span className="text-[10px] text-muted-foreground leading-none">{label}</span>
      </div>
    );
  }
  return (
    <div className={cn("flex flex-col items-start gap-0.5", isEditable && "cursor-pointer")}
      onClick={() => isEditable && setEditingKey(fieldKey)}>
      <span className={cn("text-sm font-semibold text-foreground leading-none", isEditable && "hover:text-foreground/80")}>{value}</span>
      <span className="text-[10px] text-muted-foreground leading-none">{label}</span>
    </div>
  );
}