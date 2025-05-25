import {
  Button,
  Card,
  CardActions,
  CardContent,
  Typography,
} from '@mui/material';
import { Entity } from 'entities/entity';
import React from 'react';
import { Link } from 'react-router-dom';

export interface EntityCardProps {
  entity: Entity;
  onDelete: (entity: Entity) => void;
}

export const EntityCard = ({ entity, onDelete }: EntityCardProps) => {
  return (
    <Card>
      <CardContent>
        <Typography>{entity.name}</Typography>
        <Typography>{entity.user?.login}</Typography>
      </CardContent>
      <CardActions>
        <Link to={`/entity/${entity.id}`}>
          <Button variant="outlined" size="small">
            Edit
          </Button>
        </Link>
        <Button
          variant="outlined"
          size="small"
          color="error"
          onClick={() => onDelete(entity)}
        >
          Delete
        </Button>
      </CardActions>
    </Card>
  );
};
