import { test, describe } from 'node:test';
import * as assert from 'node:assert';
import { auditVoice, buildVoiceSystemPrompt, extendProfile, DEFAULT_VOICE } from './index.ts';

describe('auditVoice', () => {
  test('returns empty array when draft passes', () => {
    const draft = 'This is a clear, useful, and honest sentence. It leads with the result.';
    const issues = auditVoice(draft);
    assert.strictEqual(issues.length, 0);
  });

  test('finds banned phrases case-insensitively', () => {
    const draft = 'Let us Delve Into the details of this paradigm shift. It is worth noting.';
    const issues = auditVoice(draft);

    const terms = issues.map(i => i.term);
    assert.ok(terms.includes('delve'));
    assert.ok(terms.includes('delve into'));
    assert.ok(terms.includes('paradigm shift'));
    assert.ok(terms.includes('it is worth noting'));
    assert.strictEqual(issues.length, 4);

    for (const issue of issues) {
      assert.strictEqual(issue.kind, 'banned');
    }
  });

  test('finds quarantined terms', () => {
    const customProfile = { ...DEFAULT_VOICE, quarantinedTerms: ['competitor brand', 'forbidden word'] };
    const draft = 'We are better than competitor brand. Do not say the forbidden word.';
    const issues = auditVoice(draft, customProfile);
    assert.strictEqual(issues.length, 2);

    const terms = issues.map(i => i.term);
    assert.ok(terms.includes('competitor brand'));
    assert.ok(terms.includes('forbidden word'));

    for (const issue of issues) {
      assert.strictEqual(issue.kind, 'quarantine');
    }
  });

  test('finds multiple occurrences of the same phrase', () => {
    const draft = 'We should delve into this. Yes, let us delve into it.';
    const issues = auditVoice(draft);

    // delve matches twice, delve into matches twice = 4 issues total
    assert.strictEqual(issues.length, 4);

    const delveIssues = issues.filter(i => i.term === 'delve');
    const delveIntoIssues = issues.filter(i => i.term === 'delve into');

    assert.strictEqual(delveIssues.length, 2);
    assert.strictEqual(delveIntoIssues.length, 2);
    assert.notStrictEqual(delveIntoIssues[0].index, delveIntoIssues[1].index);
  });
});

describe('buildVoiceSystemPrompt', () => {
  test('includes basic elements in the prompt', () => {
    const prompt = buildVoiceSystemPrompt();
    assert.ok(prompt.includes(DEFAULT_VOICE.id));
    assert.ok(prompt.includes(DEFAULT_VOICE.northStar));
    assert.ok(prompt.includes(DEFAULT_VOICE.dos[0]));
    assert.ok(prompt.includes(DEFAULT_VOICE.donts[0]));
    assert.ok(prompt.includes(DEFAULT_VOICE.bannedPhrases[0]));
  });

  test('includes channel line if channel is specified and exists', () => {
    const prompt = buildVoiceSystemPrompt(DEFAULT_VOICE, 'linkedin');
    assert.ok(prompt.includes('Channel: linkedin'));
    assert.ok(prompt.includes(DEFAULT_VOICE.channelTones?.['linkedin']!));
  });

  test('does not include channel line if channel is not found in tones', () => {
    const prompt = buildVoiceSystemPrompt(DEFAULT_VOICE, 'unknown-channel');
    assert.ok(!prompt.includes('Channel: unknown-channel'));
  });

  test('includes reference brands if present', () => {
    const customProfile = {
      ...DEFAULT_VOICE,
      referenceBrands: [{ name: 'BrandX', why: 'Because they are cool.' }]
    };
    const prompt = buildVoiceSystemPrompt(customProfile);
    assert.ok(prompt.includes('BrandX: Because they are cool.'));
  });
});

describe('extendProfile', () => {
  test('merges primitive fields and object fields correctly', () => {
    const child = extendProfile(DEFAULT_VOICE, {
      id: 'sub-brand',
      attributes: {
        newAttr: 'new value'
      },
      bannedPhrases: ['new banned phrase'],
      channelTones: {
        newChannel: 'Tone for new channel'
      }
    });

    assert.strictEqual(child.id, 'sub-brand');
    // Keeps northStar from default since it wasn't overridden
    assert.strictEqual(child.northStar, DEFAULT_VOICE.northStar);

    // Merges attributes
    assert.strictEqual(child.attributes['clarity'], DEFAULT_VOICE.attributes['clarity']);
    assert.strictEqual(child.attributes['newAttr'], 'new value');

    // Appends to arrays
    assert.ok(child.bannedPhrases.includes('delve'));
    assert.ok(child.bannedPhrases.includes('new banned phrase'));

    // Merges channels
    assert.strictEqual(child.channelTones?.['blog'], DEFAULT_VOICE.channelTones?.['blog']);
    assert.strictEqual(child.channelTones?.['newChannel'], 'Tone for new channel');
  });
});
