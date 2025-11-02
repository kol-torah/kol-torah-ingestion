import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  IconButton,
  Button,
  Stack,
  Divider,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { rabbisApi, seriesApi } from './api';
import type { Rabbi, Series, RabbiCreate, RabbiUpdate, SeriesCreate, SeriesUpdate } from './types';
import RabbiDialog from './components/RabbiDialog';
import SeriesDialog from './components/SeriesDialog';
import './App.css';

function App() {
  const [rabbis, setRabbis] = useState<Rabbi[]>([]);
  const [selectedRabbi, setSelectedRabbi] = useState<Rabbi | null>(null);
  const [series, setSeries] = useState<Series[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [rabbiDialogOpen, setRabbiDialogOpen] = useState(false);
  const [seriesDialogOpen, setSeriesDialogOpen] = useState(false);
  const [editingRabbi, setEditingRabbi] = useState<Rabbi | undefined>();
  const [editingSeries, setEditingSeries] = useState<Series | undefined>();

  // Load rabbis on mount
  useEffect(() => {
    loadRabbis();
  }, []);

  // Load series when rabbi is selected
  useEffect(() => {
    if (selectedRabbi) {
      loadSeries(selectedRabbi.id);
    } else {
      setSeries([]);
    }
  }, [selectedRabbi]);

  const loadRabbis = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await rabbisApi.getAll();
      setRabbis(response.data);
    } catch (err) {
      setError('Failed to load rabbis');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadSeries = async (rabbiId: number) => {
    try {
      setLoading(true);
      setError(null);
      const response = await seriesApi.getByRabbi(rabbiId);
      setSeries(response.data);
    } catch (err) {
      setError('Failed to load series');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRabbi = async (data: RabbiCreate) => {
    try {
      await rabbisApi.create(data);
      await loadRabbis();
    } catch (err) {
      setError('Failed to create rabbi');
      console.error(err);
    }
  };

  const handleUpdateRabbi = async (data: RabbiUpdate) => {
    if (!editingRabbi) return;
    try {
      await rabbisApi.update(editingRabbi.id, data);
      await loadRabbis();
      if (selectedRabbi?.id === editingRabbi.id) {
        const response = await rabbisApi.getById(editingRabbi.id);
        setSelectedRabbi(response.data);
      }
    } catch (err) {
      setError('Failed to update rabbi');
      console.error(err);
    }
  };

  const handleDeleteRabbi = async (rabbi: Rabbi) => {
    if (!confirm(`Delete rabbi "${rabbi.name_english}" and all their series?`)) return;
    try {
      await rabbisApi.delete(rabbi.id);
      if (selectedRabbi?.id === rabbi.id) {
        setSelectedRabbi(null);
      }
      await loadRabbis();
    } catch (err) {
      setError('Failed to delete rabbi');
      console.error(err);
    }
  };

  const handleCreateSeries = async (data: SeriesCreate) => {
    try {
      await seriesApi.create(data);
      if (selectedRabbi) {
        await loadSeries(selectedRabbi.id);
      }
    } catch (err) {
      setError('Failed to create series');
      console.error(err);
    }
  };

  const handleUpdateSeries = async (data: SeriesUpdate) => {
    if (!editingSeries) return;
    try {
      await seriesApi.update(editingSeries.id, data);
      if (selectedRabbi) {
        await loadSeries(selectedRabbi.id);
      }
    } catch (err) {
      setError('Failed to update series');
      console.error(err);
    }
  };

  const handleDeleteSeries = async (seriesItem: Series) => {
    if (!confirm(`Delete series "${seriesItem.name_english}"?`)) return;
    try {
      await seriesApi.delete(seriesItem.id);
      if (selectedRabbi) {
        await loadSeries(selectedRabbi.id);
      }
    } catch (err) {
      setError('Failed to delete series');
      console.error(err);
    }
  };

  const openCreateRabbiDialog = () => {
    setEditingRabbi(undefined);
    setRabbiDialogOpen(true);
  };

  const openEditRabbiDialog = (rabbi: Rabbi) => {
    setEditingRabbi(rabbi);
    setRabbiDialogOpen(true);
  };

  const openCreateSeriesDialog = () => {
    setEditingSeries(undefined);
    setSeriesDialogOpen(true);
  };

  const openEditSeriesDialog = (seriesItem: Series) => {
    setEditingSeries(seriesItem);
    setSeriesDialogOpen(true);
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Kol Torah Admin
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Stack direction="row" spacing={3} sx={{ height: 'calc(100vh - 200px)' }}>
        {/* Rabbis Section */}
        <Paper sx={{ flex: 1, p: 2, display: 'flex', flexDirection: 'column' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5">Rabbis</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={openCreateRabbiDialog}
            >
              Add Rabbi
            </Button>
          </Box>

          {loading && rabbis.length === 0 ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <List sx={{ flex: 1, overflow: 'auto' }}>
              {rabbis.map((rabbi) => (
                <ListItem
                  key={rabbi.id}
                  secondaryAction={
                    <Stack direction="row" spacing={0.5}>
                      <IconButton edge="end" onClick={() => openEditRabbiDialog(rabbi)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" onClick={() => handleDeleteRabbi(rabbi)}>
                        <DeleteIcon />
                      </IconButton>
                    </Stack>
                  }
                  disablePadding
                >
                  <ListItemButton
                    selected={selectedRabbi?.id === rabbi.id}
                    onClick={() => setSelectedRabbi(rabbi)}
                  >
                    <ListItemText
                      primary={rabbi.name_english}
                      secondary={rabbi.name_hebrew}
                    />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          )}
        </Paper>

        {/* Series Section */}
        <Paper sx={{ flex: 1, p: 2, display: 'flex', flexDirection: 'column' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5">
              {selectedRabbi ? `Series by ${selectedRabbi.name_english}` : 'Series'}
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={openCreateSeriesDialog}
              disabled={!selectedRabbi}
            >
              Add Series
            </Button>
          </Box>

          {!selectedRabbi ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flex: 1 }}>
              <Typography color="text.secondary">
                Select a rabbi to view their series
              </Typography>
            </Box>
          ) : loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <List sx={{ flex: 1, overflow: 'auto' }}>
              {series.length === 0 ? (
                <Box sx={{ p: 4, textAlign: 'center' }}>
                  <Typography color="text.secondary">
                    No series yet for this rabbi
                  </Typography>
                </Box>
              ) : (
                series.map((seriesItem) => (
                  <Box key={seriesItem.id}>
                    <ListItem
                      secondaryAction={
                        <Stack direction="row" spacing={0.5}>
                          <IconButton edge="end" onClick={() => openEditSeriesDialog(seriesItem)}>
                            <EditIcon />
                          </IconButton>
                          <IconButton edge="end" onClick={() => handleDeleteSeries(seriesItem)}>
                            <DeleteIcon />
                          </IconButton>
                        </Stack>
                      }
                    >
                      <ListItemText
                        primary={seriesItem.name_english}
                        secondary={
                          <>
                            <Typography component="span" variant="body2" color="text.primary">
                              {seriesItem.name_hebrew}
                            </Typography>
                            {' — '}
                            {seriesItem.type}
                            {seriesItem.description_english && (
                              <>
                                <br />
                                {seriesItem.description_english}
                              </>
                            )}
                          </>
                        }
                      />
                    </ListItem>
                    <Divider />
                  </Box>
                ))
              )}
            </List>
          )}
        </Paper>
      </Stack>

      {/* Dialogs */}
      <RabbiDialog
        open={rabbiDialogOpen}
        rabbi={editingRabbi}
        onClose={() => setRabbiDialogOpen(false)}
        onSave={editingRabbi ? handleUpdateRabbi : handleCreateRabbi}
      />

      {selectedRabbi && (
        <SeriesDialog
          open={seriesDialogOpen}
          series={editingSeries}
          rabbiId={selectedRabbi.id}
          onClose={() => setSeriesDialogOpen(false)}
          onSave={editingSeries ? handleUpdateSeries : handleCreateSeries}
        />
      )}
    </Container>
  );
}

export default App;
