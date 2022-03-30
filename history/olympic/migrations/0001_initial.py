# Generated by Django 3.2.12 on 2022-03-30 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id_event', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id_game', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('season', models.CharField(choices=[('WT', 'Winter'), ('SM', 'Summer')], default='SM', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id_nationality', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id_sport', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id_team', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id_person', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='olympic.nationality')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='olympic.team')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipationGame',
            fields=[
                ('id_participation', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medal', models.CharField(choices=[('NA', 'N/A'), ('BZ', 'Bronze'), ('SV', 'Silver'), ('GD', 'Gold')], default='NA', max_length=2)),
                ('events', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='olympic.event')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='olympic.game')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='olympic.person')),
            ],
        ),
    ]