import { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Stack,
} from '@mui/material';
import type { Rabbi, RabbiCreate, RabbiUpdate } from '../types';

interface RabbiDialogProps {
  open: boolean;
  rabbi?: Rabbi;
  onClose: () => void;
  onSave: (data: RabbiCreate | RabbiUpdate) => Promise<void>;
}

export default function RabbiDialog({ open, rabbi, onClose, onSave }: RabbiDialogProps) {
  const [formData, setFormData] = useState<RabbiCreate>({
    name_hebrew: rabbi?.name_hebrew || '',
    name_english: rabbi?.name_english || '',
    slug: rabbi?.slug || '',
    website_url: rabbi?.website_url || '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSave(formData);
    onClose();
  };

  const handleChange = (field: keyof RabbiCreate) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>{rabbi ? 'Edit Rabbi' : 'Create New Rabbi'}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <TextField
              label="Name (Hebrew)"
              value={formData.name_hebrew}
              onChange={handleChange('name_hebrew')}
              required
              fullWidth
            />
            <TextField
              label="Name (English)"
              value={formData.name_english}
              onChange={handleChange('name_english')}
              required
              fullWidth
            />
            <TextField
              label="Slug"
              value={formData.slug}
              onChange={handleChange('slug')}
              required
              fullWidth
              helperText="URL-friendly identifier (e.g., rabbi-shlomo-katz)"
            />
            <TextField
              label="Website URL"
              value={formData.website_url}
              onChange={handleChange('website_url')}
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained">
            {rabbi ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
