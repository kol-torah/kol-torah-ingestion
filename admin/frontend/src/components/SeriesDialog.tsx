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
import type { Series, SeriesCreate, SeriesUpdate } from '../types';

interface SeriesDialogProps {
  open: boolean;
  series?: Series;
  rabbiId: number;
  onClose: () => void;
  onSave: (data: SeriesCreate | SeriesUpdate) => Promise<void>;
}

export default function SeriesDialog({ open, series, rabbiId, onClose, onSave }: SeriesDialogProps) {
  const [formData, setFormData] = useState<SeriesCreate>({
    rabbi_id: series?.rabbi_id || rabbiId,
    name_hebrew: series?.name_hebrew || '',
    name_english: series?.name_english || '',
    description_hebrew: series?.description_hebrew || '',
    description_english: series?.description_english || '',
    website_url: series?.website_url || '',
    type: series?.type || '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSave(formData);
    onClose();
  };

  const handleChange = (field: keyof SeriesCreate) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>{series ? 'Edit Series' : 'Create New Series'}</DialogTitle>
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
              label="Type"
              value={formData.type}
              onChange={handleChange('type')}
              required
              fullWidth
              helperText="e.g., Parsha, Holidays, Halacha"
            />
            <TextField
              label="Description (Hebrew)"
              value={formData.description_hebrew}
              onChange={handleChange('description_hebrew')}
              multiline
              rows={3}
              fullWidth
            />
            <TextField
              label="Description (English)"
              value={formData.description_english}
              onChange={handleChange('description_english')}
              multiline
              rows={3}
              fullWidth
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
            {series ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
